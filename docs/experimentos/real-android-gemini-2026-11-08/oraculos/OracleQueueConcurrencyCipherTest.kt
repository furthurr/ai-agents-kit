// Contrato de pruebas anonimizado: nombres sintéticos; no acredita una nueva ejecución del proyecto original.
package com.example.mobilefixture.data.local.offline

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.runBlocking
import com.example.mobilefixture.data.local.offline.dao.PendingActionDao
import com.example.mobilefixture.data.local.offline.entity.PendingActionEntity
import com.example.mobilefixture.domain.offline.capture.TipoDeAlta
import com.example.mobilefixture.domain.offline.queue.EstadoPendiente
import com.example.mobilefixture.domain.offline.queue.PendingAction
import com.example.mobilefixture.security.crypto.WrappedKeyCipher
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test
import org.mockito.kotlin.any
import org.mockito.kotlin.mock
import org.mockito.kotlin.whenever

/**
 * Oráculo de evaluación externa independiente para la Tarea 3: Alta (GBA-QUEUE-CONCURRENCY-CIPHER).
 * Valida deduplicación atómica, cifrado obligatorio por campo y recuperación segura de bloqueos.
 */
class OracleQueueConcurrencyCipherTest {

    private class FakePendingActionDao {
        val lock = Any()
        val entities = mutableMapOf<String, PendingActionEntity>()

        suspend fun insertar(accion: PendingActionEntity) {
            synchronized(lock) { entities[accion.idLocal] = accion }
        }

        suspend fun listarFifo(): List<PendingActionEntity> = synchronized(lock) {
            entities.values.sortedWith(compareBy({ it.timestamp }, { it.idLocal })).toList()
        }

        suspend fun listarPorEstado(estado: String): List<PendingActionEntity> = synchronized(lock) {
            entities.values.filter { it.estado == estado }
                .sortedWith(compareBy({ it.timestamp }, { it.idLocal })).toList()
        }

        suspend fun actualizarEstado(idLocal: String, estado: String, ahora: Long) {
            synchronized(lock) {
                entities[idLocal]?.let {
                    entities[idLocal] = it.copy(estado = estado, actualizadoEn = ahora)
                }
            }
        }

        suspend fun actualizarEstadoConMotivo(idLocal: String, estado: String, motivo: String?, ahora: Long) {
            synchronized(lock) {
                entities[idLocal]?.let {
                    entities[idLocal] = it.copy(estado = estado, motivoError = motivo, actualizadoEn = ahora)
                }
            }
        }

        suspend fun reemplazarPayload(idLocal: String, payloadCifrado: String, estado: String, ahora: Long) {
            synchronized(lock) {
                entities[idLocal]?.let {
                    entities[idLocal] = it.copy(payloadCifrado = payloadCifrado, estado = estado, motivoError = null, actualizadoEn = ahora)
                }
            }
        }

        suspend fun incrementarIntentos(idLocal: String) {
            synchronized(lock) {
                entities[idLocal]?.let {
                    entities[idLocal] = it.copy(intentos = it.intentos + 1)
                }
            }
        }

        suspend fun intentosDe(idLocal: String): Int? = synchronized(lock) {
            entities[idLocal]?.intentos
        }

        suspend fun contarPorEstados(estados: List<String>): Int = synchronized(lock) {
            entities.values.count { it.estado in estados }
        }

        suspend fun purgarAnterioresA(estado: String, limiteMillis: Long) {
            synchronized(lock) {
                entities.values.filter { it.estado == estado && it.actualizadoEn < limiteMillis }
                    .map { it.idLocal }
                    .forEach { entities.remove(it) }
            }
        }

        suspend fun eliminar(idLocal: String) {
            synchronized(lock) { entities.remove(idLocal) }
        }

        suspend fun borrarTodo() {
            synchronized(lock) { entities.clear() }
        }

        suspend fun listarTodas(): List<PendingActionEntity> = listarFifo()

        suspend fun recuperarCandadosHuerfanos(limiteMillis: Long, ahora: Long): Int = synchronized(lock) {
            val stale = entities.values.filter {
                it.estado == EstadoPendiente.ENVIANDO.name && it.actualizadoEn < limiteMillis
            }
            stale.forEach { entities[it.idLocal] = it.copy(
                estado = EstadoPendiente.PENDIENTE.name, actualizadoEn = ahora) }
            stale.size
        }

        // Structural adapter: additive interface members no longer break compilation.
        // Unsupported operations fail explicitly; no permissive mock defaults.
        val adapter: PendingActionDao = java.lang.reflect.Proxy.newProxyInstance(
            PendingActionDao::class.java.classLoader, arrayOf(PendingActionDao::class.java)
        ) { _, method, args ->
            val implementation = javaClass.methods.singleOrNull {
                it.name == method.name && it.parameterTypes.contentEquals(method.parameterTypes)
            } ?: error("Unsupported oracle DAO operation: ${method.name}")
            try {
                implementation.invoke(this, *args.orEmpty())
            } catch (error: java.lang.reflect.InvocationTargetException) {
                throw error.targetException
            }
        } as PendingActionDao
    }

    private lateinit var daoFake: FakePendingActionDao
    private val cipherMock = mock<WrappedKeyCipher>()

    @Before
    fun setUp() {
        daoFake = FakePendingActionDao()

        whenever(cipherMock.encrypt(any())).thenAnswer { invocation ->
            val arg = invocation.getArgument<String>(0)
            "CIPHERED_" + java.util.Base64.getEncoder().encodeToString(arg.reversed().toByteArray())
        }
        whenever(cipherMock.decrypt(any())).thenAnswer { invocation ->
            val arg = invocation.getArgument<String>(0)
            if (arg.startsWith("CIPHERED_")) {
                String(java.util.Base64.getDecoder().decode(arg.removePrefix("CIPHERED_"))).reversed()
            } else {
                arg
            }
        }
    }

    private fun createStore(): OfflineQueueStore {
        return OfflineQueueStore(daoFake.adapter, cipherMock)
    }

    @Test
    fun oraculo01_cifradoObligatorioDePiiEnPersistencia() = runBlocking {
        val store = createStore()
        val accion = PendingAction(
            idLocal = "uuid-123",
            tipoDeAlta = TipoDeAlta("PROSPECTO"),
            idEjecutivo = "EMP001",
            payload = "{\"nombre\":\"Pedro Perez\",\"ingresos\":50000}",
            estado = EstadoPendiente.PENDIENTE,
            timestamp = 1000L,
            rfc = "PEP900101AA1"
        )

        val idRetornado = store.insertarIdempotente(accion)
        assertEquals("uuid-123", idRetornado)

        val entity = daoFake.entities["uuid-123"]
        assertNotNull("La entidad debió ser insertada", entity)
        entity!!

        // Ningún dato personal sensible debe quedar en claro
        assertFalse("El payload no debe estar en texto plano", entity.payloadCifrado.contains("Pedro Perez"))
        assertFalse("El idEjecutivo no debe estar en texto plano", entity.idEjecutivoCifrado.contains("EMP001"))
        assertFalse("El RFC no debe estar en texto plano", entity.rfcCifrado?.contains("PEP900101") ?: false)

        assertTrue(entity.payloadCifrado.startsWith("CIPHERED_"))
        assertTrue(entity.idEjecutivoCifrado.startsWith("CIPHERED_"))
    }

    @Test
    fun oraculo02_deduplicacionLogicaYAtomicidadEnConcurrencia() = runBlocking {
        val store = createStore()
        val accion1 = PendingAction(
            idLocal = "local-1",
            tipoDeAlta = TipoDeAlta("PROSPECTO"),
            idEjecutivo = "EMP001",
            payload = "{\"razonSocial\":\"Empresa 1\"}",
            estado = EstadoPendiente.PENDIENTE,
            timestamp = 1000L,
            rfc = "EMP900101AA1"
        )
        val accion2 = PendingAction(
            idLocal = "local-2",
            tipoDeAlta = TipoDeAlta("PROSPECTO"),
            idEjecutivo = "EMP001",
            payload = "{\"razonSocial\":\"Empresa 1 Duplicada\"}",
            estado = EstadoPendiente.PENDIENTE,
            timestamp = 2000L,
            rfc = "EMP900101AA1"
        )

        // 10 corutinas simultáneas intentando insertar la misma alta
        val resultados = (1..10).map {
            async(Dispatchers.Default) {
                store.insertarIdempotente(if (it % 2 == 0) accion1 else accion2)
            }
        }.awaitAll()

        // Todas deben retornar el mismo idLocal (la primera insertada)
        val idPrimero = resultados.first()
        assertTrue("Todas las llamadas concurrentes deben devolver el mismo idLocal", resultados.all { it == idPrimero })
        assertEquals("La entidad no debe haberse duplicado físicamente en el DAO", 1, daoFake.entities.size)
    }

    @Test
    fun oraculo04_tiposDistintosNoSeDeduplican() = runBlocking {
        val store = createStore()
        val first = PendingAction(idLocal = "tipo-1", tipoDeAlta = TipoDeAlta("PROSPECTO"),
            idEjecutivo = "EMP001", payload = "{}", estado = EstadoPendiente.PENDIENTE,
            timestamp = 1000L, rfc = "EMP900101AA1")
        assertEquals("tipo-1", store.insertarIdempotente(first))
        assertEquals("tipo-2", store.insertarIdempotente(first.copy(
            idLocal = "tipo-2", tipoDeAlta = TipoDeAlta("CLIENTE"))))
        assertEquals(2, daoFake.entities.size)
    }

    @Test
    fun oraculo03_recuperacionSeguraDeCandadosHuerfanos() = runBlocking {
        val store = createStore()
        val ahora = 100_000L
        val timeout = 10_000L

        // Entidad huérfana (ENVIANDO desde hace más de 10s)
        val huerfana = PendingActionEntity(
            idLocal = "huerfana-1", tipoDeAlta = "PROSPECTO", idEjecutivoCifrado = "CIPHERED[1]",
            payloadCifrado = "CIPHERED[{}]", estado = EstadoPendiente.ENVIANDO.name,
            timestamp = 50_000L, actualizadoEn = 80_000L, intentos = 1
        )
        // Entidad activa reciente (ENVIANDO desde hace 2s)
        val reciente = PendingActionEntity(
            idLocal = "reciente-1", tipoDeAlta = "PROSPECTO", idEjecutivoCifrado = "CIPHERED[1]",
            payloadCifrado = "CIPHERED[{}]", estado = EstadoPendiente.ENVIANDO.name,
            timestamp = 95_000L, actualizadoEn = 98_000L, intentos = 1
        )
        // Entidad en conflicto que NUNCA debe tocarse
        val conflicto = PendingActionEntity(
            idLocal = "conflicto-1", tipoDeAlta = "PROSPECTO", idEjecutivoCifrado = "CIPHERED[1]",
            payloadCifrado = "CIPHERED[{}]", estado = EstadoPendiente.CONFLICTO.name,
            timestamp = 50_000L, actualizadoEn = 50_000L, intentos = 1
        )

        daoFake.entities[huerfana.idLocal] = huerfana
        daoFake.entities[reciente.idLocal] = reciente
        daoFake.entities[conflicto.idLocal] = conflicto

        val recuperadas = store.recuperarCandadosHuerfanos(timeout, ahora)
        assertEquals("Debe recuperar exactamente 1 candado huérfano", 1, recuperadas)

        // Verificar estados en daoFake
        assertEquals(EstadoPendiente.PENDIENTE.name, daoFake.entities["huerfana-1"]?.estado)
        assertEquals(EstadoPendiente.ENVIANDO.name, daoFake.entities["reciente-1"]?.estado)
        assertEquals(EstadoPendiente.CONFLICTO.name, daoFake.entities["conflicto-1"]?.estado)
    }
}
