// Contrato de pruebas anonimizado: nombres sintéticos; no acredita una nueva ejecución del proyecto original.
package com.example.mobilefixture.tests1.features.offline.buzon

import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.launch
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.runTest
import com.example.mobilefixture.domain.offline.capture.TipoDeAlta
import com.example.mobilefixture.domain.offline.connectivity.OfflineConnectivityGateway
import com.example.mobilefixture.domain.offline.connectivity.OfflineConnectivityState
import com.example.mobilefixture.domain.offline.queue.AlmacenColaOffline
import com.example.mobilefixture.domain.offline.queue.EstadoPendiente
import com.example.mobilefixture.domain.offline.queue.PendingAction
import com.example.mobilefixture.domain.offline.queue.PendingActionsQueue
import com.example.mobilefixture.tests1.features.offline.InterruptorOffline
import com.example.mobilefixture.tests1.features.offline.sync.EnvioAltaPorTipo
import com.example.mobilefixture.tests1.util.MainDispatcherRule
import com.example.mobilefixture.security.storage.SecureStorage
import com.example.mobilefixture.security.util.UserKeys
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.mockito.kotlin.any
import org.mockito.kotlin.doReturn
import org.mockito.kotlin.mock
import org.mockito.kotlin.never
import org.mockito.kotlin.verify
import org.mockito.kotlin.whenever
import org.robolectric.RobolectricTestRunner
import java.io.IOException

/**
 * Oráculo de evaluación externa independiente para la Tarea 2: Media-Alta (GBA-BUZON-RETRY-UI).
 * Valida la remediación de QLT-0017 y la acción de reintento de altas en conflicto.
 */
@OptIn(ExperimentalCoroutinesApi::class)
@RunWith(RobolectricTestRunner::class)
class OracleBuzonRetryUiTest {

    @get:Rule val main = MainDispatcherRule()

    private val colaMock = mock<PendingActionsQueue>()
    private val secureStorageMock = mock<SecureStorage>()
    private val conectividadMock = mock<OfflineConnectivityGateway> {
        on { observe() } doReturn flowOf(OfflineConnectivityState.EnLinea)
    }
    private val envioMock = mock<EnvioAltaPorTipo>()
    private val almacenMock = mock<AlmacenColaOffline>()

    @Before
    fun setUp() {
        whenever(secureStorageMock.getString(UserKeys.EMPLOYEE_NUMBER)).thenReturn("998877")
    }

    @Test
    fun oraculo01_falloDeLecturaDeColaNoOcultaAccesoAlBuzon() = runTest(main.dispatcher) {
        // Simular un fallo grave de base de datos / descifrado
        whenever(colaMock.todas()).thenAnswer { throw IOException("SQLite database locked or corrupted") }

        val vm = AccesoBuzonViewModel(colaMock, secureStorageMock)
        vm.refrescar()
        advanceUntilIdle()

        // Remediación QLT-0017: hayAltas debe mantenerse visible (true) ante error para no apagar el Buzón
        assertTrue("Ante fallo de lectura, el acceso al Buzón debe permanecer visible (hayAltas == true)", vm.hayAltas.value)
        assertEquals("El contador de pendientes debe ser 0 ante fallo", 0, vm.porEnviar.value)
    }

    @Test
    fun oraculo02_estadoAccesoExponeErrorTipado() = runTest(main.dispatcher) {
        val causa = IOException("Disk error")
        whenever(colaMock.todas()).thenAnswer { throw causa }

        val vm = AccesoBuzonViewModel(colaMock, secureStorageMock)
        vm.refrescar()
        advanceUntilIdle()

        assertTrue("El estado debe indicar Error", vm.estadoAcceso.value is EstadoAccesoBuzon.Error)
    }

    @Test
    fun oraculo03_reintentarEnAccesoBuzonVuelveAEjecutarLectura() = runTest(main.dispatcher) {
        val accion = PendingAction(
            idLocal = "act-1", tipoDeAlta = TipoDeAlta("PROSPECTO"), idEjecutivo = "998877",
            payload = "{}", estado = EstadoPendiente.PENDIENTE, timestamp = 1000L
        )

        whenever(colaMock.todas())
            .thenAnswer { throw IOException("Timeout inicial") }
            .thenReturn(listOf(accion))

        val vm = AccesoBuzonViewModel(colaMock, secureStorageMock)
        vm.refrescar()
        advanceUntilIdle()

        assertTrue(vm.estadoAcceso.value is EstadoAccesoBuzon.Error)

        vm.reintentar()
        advanceUntilIdle()

        assertEquals(1, vm.porEnviar.value)
        assertTrue(vm.hayAltas.value)
        assertTrue(vm.estadoAcceso.value is EstadoAccesoBuzon.Exito)
    }

    @Test
    fun oraculo04_reintentarAltaEnConflictoTransicionaAPendiente() = runTest(main.dispatcher) {
        val accionEnConflicto = PendingAction(
            idLocal = "conf-99", tipoDeAlta = TipoDeAlta("PROSPECTO"), idEjecutivo = "998877",
            payload = "{}", estado = EstadoPendiente.CONFLICTO, timestamp = 1000L,
            motivoError = "RFC duplicado en servidor"
        )
        whenever(colaMock.todas()).thenReturn(listOf(accionEnConflicto))

        val vm = BuzonSalidaViewModel(
            colaCompleta = colaMock,
            conectividad = conectividadMock,
            envio = envioMock,
            secureStorage = secureStorageMock,
            descripciones = null,
            almacen = almacenMock
        )

        backgroundScope.launch { vm.estado.collect {} }
        advanceUntilIdle()

        vm.reintentarAltaEnConflicto("conf-99")
        advanceUntilIdle()

        verify(almacenMock).actualizarEstadoConMotivo("conf-99", EstadoPendiente.PENDIENTE, null)
    }
}
