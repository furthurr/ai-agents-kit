//
//  OracleQueueConcurrencyCipherTests.swift
//  FixtureProject Tests
//
//  Oráculo externo para verificar la Tarea 3: GIOS-QUEUE-CONCURRENCY-CIPHER
//

import XCTest
@testable import FixtureModule

final class OracleQueueConcurrencyCipherTests: XCTestCase {

    private var sut: FixtureComponent1!

    override func setUp() {
        super.setUp()
        sut = FixtureComponent1()
        sut.clearAll()
    }

    override func tearDown() {
        sut.clearAll()
        sut = nil
        super.tearDown()
    }

    func testEnqueueIdempotente_mismoPayload_noDuplica() {
        let action1 = FixtureComponent2(action: "crear_prospecto", entityName: "prospecto", payload: "RFC_SECRETO_12345", status: .pending)
        let action2 = FixtureComponent2(action: "crear_prospecto", entityName: "prospecto", payload: "RFC_SECRETO_12345", status: .pending)

        let id1 = sut.enqueueIdempotente(action: action1)
        let id2 = sut.enqueueIdempotente(action: action2)

        XCTAssertEqual(id1, id2, "Debe retornar el mismo UUID de la acción existente")
        XCTAssertEqual(sut.loadAll().count, 1, "No debe duplicar elementos en la cola")
    }

    func testEnqueueIdempotente_concurrencia_threadSafe() {
        let iterations = 20
        var returnedIds = [UUID]()
        let lock = NSLock()

        DispatchQueue.concurrentPerform(iterations: iterations) { _ in
            let action = FixtureComponent2(
                action: "alta_concurrente",
                entityName: "cliente",
                payload: "{\"cuenta\":\"1234567890\"}",
                status: .pending
            )
            let id = sut.enqueueIdempotente(action: action)
            lock.lock()
            returnedIds.append(id)
            lock.unlock()
        }

        XCTAssertEqual(returnedIds.count, iterations)
        let uniqueIds = Set(returnedIds)
        XCTAssertEqual(uniqueIds.count, 1, "Todas las operaciones concurrentes deben deduplicar al mismo ID")
        XCTAssertEqual(sut.loadAll().count, 1, "La cola en disco debe contener exactamente 1 elemento")
    }

    func testCifradoTransparente_payloadAlmacenadoNoEnTextoPlano() {
        let payloadSecreto = "CONFIDENCIAL_PII_987654321"
        let action = FixtureComponent2(action: "guardar_secreto", entityName: "seguridad", payload: payloadSecreto, status: .pending)

        _ = sut.enqueueIdempotente(action: action)

        // 1. Verificación de descifrado transparente para consumidores
        let cargados = sut.loadAll()
        XCTAssertEqual(cargados.first?.payload, payloadSecreto)

        // 2. Verificación de cifrado en reposo (UserDefaults crudo)
        if let rawData = UserDefaults.standard.data(forKey: "benchmark.fixture.queue"),
           let rawString = String(data: rawData, encoding: .utf8) {
            XCTAssertFalse(rawString.contains(payloadSecreto), "El payload NO debe guardarse en texto plano en disco")
        }
    }
}
