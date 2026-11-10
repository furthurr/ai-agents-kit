// Contrato de pruebas anonimizado: nombres sintéticos; no acredita una nueva ejecución del proyecto original.
package com.example.mobilefixture.domain.use_case.prospect

import com.example.mobilefixture.domain.model.prospect.Prospect
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Oráculo de evaluación externa independiente para la Tarea 1: Media-Baja (GBA-SEARCH-PROSPECTS).
 * No es visible para los participantes durante la inferencia.
 */
class OracleSearchProspectsTest {

    // Instanciación directa o por reflexión si es clase concreta
    private fun createUseCase(): FixtureSource1 {
        val clazz = try {
            Class.forName("com.example.mobilefixture.domain.use_case.prospect.FixtureSource1Impl")
        } catch (_: ClassNotFoundException) {
            Class.forName("com.example.mobilefixture.domain.use_case.prospect.FixtureSource1Kt")
        }
        return clazz.getDeclaredConstructor().newInstance() as FixtureSource1
    }

    private val p1 = Prospect(id = "1", razonSocial = "Comercializadora González S.A.", rfc = "CGO850101AA1", nombreEmpleado = "Juan Pérez", tipoCliente = "PYME", marcaGestion = "1")
    private val p2 = Prospect(id = "2", razonSocial = "Abarrotes Pérez y López", rfc = "APL900202BB2", nombreEmpleado = "María Gómez", tipoCliente = "CORPORATIVO", marcaGestion = "0")
    private val p3 = Prospect(id = "3", razonSocial = "Empresa Digital Demo", rfc = "DEMO000303CC3", nombreEmpleado = "Carlos Sánchez", tipoCliente = "PYME", marcaGestion = "S")
    private val p4 = Prospect(id = "4", razonSocial = null, rfc = "ZZZ999999ZZ9", nombreEmpleado = "Sin Razón Social", tipoCliente = "PYME", marcaGestion = null)
    private val p5 = Prospect(id = "5", razonSocial = "Distribuidora Ávalos", rfc = "DAV700101DD4", nombreEmpleado = "Ana Ramos", tipoCliente = "GOBIERNO", marcaGestion = "")

    private val baseList = listOf(p1, p2, p3, p4, p5)

    @Test
    fun oraculo01_busquedaPorRazonSocialConAcentosEInsensibleAMayusculas() {
        val useCase = createUseCase()
        // Buscar sin acento debe encontrar "González"
        val res = useCase(baseList, query = "gonzalez")
        assertEquals(1, res.items.size)
        assertEquals("1", res.items[0].id)
    }

    @Test
    fun oraculo02_busquedaConAcentoEncuentraTextoSinAcento() {
        val useCase = createUseCase()
        // Buscar con acento "PÉREZ" debe encontrar "Pérez y López"
        val res = useCase(baseList, query = "PÉREZ")
        // También p1 tiene nombreEmpleado = Juan Pérez, por lo que ambos deben coincidir
        assertEquals(2, res.items.size)
    }

    @Test
    fun oraculo03_busquedaPorRfc() {
        val useCase = createUseCase()
        val res = useCase(baseList, query = "demo000")
        assertEquals(1, res.items.size)
        assertEquals("3", res.items[0].id)
    }

    @Test
    fun oraculo04_busquedaPorNombreEmpleado() {
        val useCase = createUseCase()
        val res = useCase(baseList, query = "carlos")
        assertEquals(1, res.items.size)
        assertEquals("3", res.items[0].id)
    }

    @Test
    fun oraculo05_queryVacioOEspaciosRetornaTodosOrdenados() {
        val useCase = createUseCase()
        val res = useCase(baseList, query = "   ")
        assertEquals(5, res.items.size)
        assertEquals(5, res.totalCount)
    }

    @Test
    fun oraculo06_filtroPorTipoCliente() {
        val useCase = createUseCase()
        val res = useCase(baseList, tipoCliente = "pyme")
        assertEquals(3, res.items.size)
        assertTrue(res.items.all { it.tipoCliente.equals("pyme", ignoreCase = true) })
    }

    @Test
    fun oraculo07_filtroSoloGestionadosExcluyeNulosVaciosYCeros() {
        val useCase = createUseCase()
        val res = useCase(baseList, soloGestionados = true)
        // p1 (marcaGestion="1") y p3 (marcaGestion="S") son válidos
        // p2 (0), p4 (null) y p5 ("") deben quedar excluidos
        assertEquals(2, res.items.size)
        assertTrue(res.items.any { it.id == "1" })
        assertTrue(res.items.any { it.id == "3" })
    }

    @Test
    fun oraculo08_ordenamientoAlfabéticoConAcentosYNulosAlFinal() {
        val useCase = createUseCase()
        val res = useCase(baseList)
        // Orden esperado de razón social:
        // 1. Abarrotes Pérez y López
        // 2. Comercializadora González S.A.
        // 3. Distribuidora Ávalos
        // 4. Empresa Digital Demo
        // 5. null (p4 va al final)
        assertEquals("2", res.items[0].id)
        assertEquals("1", res.items[1].id)
        assertEquals("5", res.items[2].id)
        assertEquals("3", res.items[3].id)
        assertEquals("4", res.items[4].id)
    }

    @Test
    fun oraculo09_calculoDeMetricasTotalYGestionados() {
        val useCase = createUseCase()
        val res = useCase(baseList, tipoCliente = "PYME")
        // Items PYME: p1 (gestionado="1"), p3 (gestionado="S"), p4 (gestionado=null)
        assertEquals(3, res.totalCount)
        assertEquals(2, res.gestionadosCount)
    }

    @Test
    fun oraculo10_listaVaciaRetornaResultadoLimpio() {
        val useCase = createUseCase()
        val res = useCase(emptyList(), query = "algo", tipoCliente = "PYME", soloGestionados = true)
        assertEquals(0, res.items.size)
        assertEquals(0, res.totalCount)
        assertEquals(0, res.gestionadosCount)
    }
}
