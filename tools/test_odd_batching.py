import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

import gemini_three_way
import odd_batching as lab
import odd_batching_report as report


def finish(input=1, output=2, read=3, write=0, reason='stop'):
    return {'type':'step_finish','part':{'type':'step-finish','reason':reason,
            'tokens':{'input':input,'output':output,'reasoning':4,'cache':{'read':read,'write':write}}}}


def tool(name,data,output='',status='completed'):
    return {'type':'tool_use','part':{'type':'tool','tool':name,'state':{'input':data,'output':output,'status':status}}}


class FakeProcess:
    def __init__(self, events):
        self.stdout=io.BytesIO(('\n'.join(json.dumps(e) for e in events)+'\n').encode())
        self.stderr=io.BytesIO(b'not persisted')
        self.returncode=0
        self.pid=123456789

    def poll(self):return self.returncode
    def wait(self):return self.returncode


class MetricsTests(unittest.TestCase):
    def test_exact_formula_reasoning_separate(self):
        self.assertEqual(lab.metric(finish()['part'])['comparable_tokens'],6)
        self.assertEqual(lab.metric(finish()['part'])['reasoning'],4)

    def test_missing_metrics_are_unknown(self):
        value=finish()
        del value['part']['tokens']['cache']['read']
        self.assertIsNone(lab.metric(value['part']))
        result=lab.totals([finish(),value])
        self.assertFalse(result['complete'])
        self.assertEqual(result['observed']['comparable_tokens'],6)
        self.assertEqual(result['measured_steps'],1)

    def test_no_steps_not_zero(self):
        self.assertIsNone(lab.totals([])['observed'])
        self.assertFalse(lab.totals([])['complete'])

    def test_negative_metric_invalid(self):
        self.assertIsNone(lab.metric(finish(read=-1)['part']))


class BudgetTests(unittest.TestCase):
    def test_four_calls_only(self):
        b=lab.Budget()
        for _ in range(4):b.reserve(None)
        with self.assertRaises(RuntimeError):b.reserve(None)

    def test_no_resume(self):
        with self.assertRaises(RuntimeError):lab.Budget().reserve('session')

    def test_halt_prevents_new_call(self):
        b=lab.Budget();b.halt('api');b.halt('api')
        self.assertEqual(b.reasons,['api'])
        with self.assertRaises(RuntimeError):b.reserve(None)


class TransportTests(unittest.TestCase):
    def invoke(self,events,budget=None):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            def write_json(path,value,exclusive=False):
                path.parent.mkdir(parents=True,exist_ok=True)
                with path.open('x' if exclusive else 'w') as file:json.dump(value,file)
            base=types.SimpleNamespace(CLI='never-called',configuration=lambda *args:{},make_exec_env=lambda cfg:{},
                agent_name=lambda arm:arm,stamp=lambda:'stamp',kit_bench=gemini_three_way,
                write_json=write_json,text_sha=gemini_three_way.text_sha)
            b=budget or lab.Budget()
            with patch.object(lab.subprocess,'Popen',return_value=FakeProcess(events)) as popen:
                result=lab.invoke(base,b,root,'odd',root/'cell','prompt')
            saved=json.loads((root/'transport/cell.json').read_text())
            return result,b,saved,popen.call_args

    def test_success_identity_and_safe_events(self):
        result,b,saved,args=self.invoke([{'type':'reasoning','part':{'type':'reasoning','text':'PRIVATE'}},finish()])
        self.assertEqual(b.calls,1)
        self.assertEqual(result['measurement']['observed']['comparable_tokens'],6)
        self.assertNotIn('PRIVATE',json.dumps(saved))
        self.assertIn('--variant',args.args[0]);self.assertIn('max',args.args[0])
        self.assertEqual(result['stderr_bytes'],13)
        self.assertNotIn('not persisted',json.dumps(saved))

    def test_403_stops_cohort_and_preserves_status(self):
        result,b,_,_=self.invoke([{'type':'error','error':{'name':'APIError','data':{'statusCode':403,'message':'not retained'}}}])
        self.assertTrue(b.stop.is_set())
        self.assertEqual(result['events'][0]['error']['statusCode'],403)
        self.assertEqual(result['stop_reason'],'api_or_process_error')
        self.assertIsNone(result['measurement']['observed'])

    def test_token_boundary_stop(self):
        with patch.object(lab,'TOKEN_LIMIT',5):
            result,b,_,_=self.invoke([finish()])
        self.assertEqual(result['stop_reason'],'token_budget')
        self.assertTrue(b.stop.is_set())

    def test_missing_counter_stops(self):
        event=finish();del event['part']['tokens']['output']
        result,b,_,_=self.invoke([event])
        self.assertEqual(result['stop_reason'],'incomplete_metrics')
        self.assertTrue(b.stop.is_set())

    def test_step_limit_stop_unfinished(self):
        with patch.object(lab,'STEP_LIMIT',1):
            result,_,_,_=self.invoke([finish(reason='tool-calls')])
        self.assertEqual(result['stop_reason'],'step_budget')

    def test_exact_limit_natural_finish_allowed(self):
        with patch.object(lab,'STEP_LIMIT',1):
            result,b,_,_=self.invoke([finish()])
        self.assertIsNone(result['stop_reason'])
        self.assertFalse(b.stop.is_set())

    def test_non_object_event_stream_stops(self):
        result,b,saved,_=self.invoke(['unexpected event',finish()])
        self.assertEqual(result['stop_reason'],'invalid_event_stream')
        self.assertTrue(b.stop.is_set())
        self.assertEqual(len(saved['invalid_stdout_lines']),1)
        self.assertNotIn('unexpected event',json.dumps(saved))


class ReportTests(unittest.TestCase):
    def test_mixed_patch_multilabel(self):
        event=tool('apply_patch',{'patchText':'*** Begin Patch\n*** Update File: catalog/views.py\n*** Add File: catalog/tests/test_x.py\n*** End Patch'})
        result=report.inspect_events([event,finish()])
        self.assertEqual(result['operation_counts']['product-write'],1)
        self.assertEqual(result['operation_counts']['test-write'],1)
        self.assertEqual(result['operation_counts']['mixed-patch'],1)

    def test_grouping_and_read_repeats(self):
        event=tool('read',{'filePath':'views.py'})
        result=report.inspect_events([event,event,finish()])
        self.assertEqual(result['rounds_with_multiple_tools'],1)
        self.assertEqual(result['tool_calls'],2)
        self.assertEqual(result['exact_read_repeats'][0]['count'],2)

    def test_note_not_product(self):
        event=tool('write',{'filePath':'odd/tasks/feature.md'})
        result=report.inspect_events([event,finish()])
        self.assertIsNone(result['first_product_event'])
        self.assertEqual(result['operation_counts']['note-write'],1)

    def test_kernel_removes_only_automatic_plan_followup(self):
        source="prefix\n    if arm != 'sdd' and kit_bench.healthy(result) and initial_product == product_hashes(workspace):\n        message('approve-plan')\n\n    if arm == 'sdd' and selected_mode == 'tiny':\n        suffix\n"
        transformed=lab.stripped_kernel(source)
        self.assertNotIn("'approve-plan'",transformed)
        self.assertTrue(transformed.startswith('prefix'))
        self.assertTrue(transformed.endswith('        suffix\n'))


if __name__=='__main__':unittest.main()
