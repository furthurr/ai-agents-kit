// Contrato de pruebas anonimizado: nombres sintéticos; no acredita una nueva ejecución del proyecto original.
//
//  OracleBuzonRetryUiTests.swift
//  FixtureProject Tests
//
//  Oráculo externo para verificar la Tarea 2: GIOS-BUZON-RETRY-UI
//

import XCTest
@testable import FixtureModule

final class OracleBuzonRetryUiTests: XCTestCase {

    private var queue: FixtureComponent1!
    private var sut: BuzonSalidaViewModel!

    override func setUp() {
        super.setUp()
        queue = FixtureComponent1()
        queue.clearAll()
        sut = BuzonSalidaViewModel(queue: queue)
    }

    override func tearDown() {
        queue.clearAll()
        sut = nil
        queue = nil
        super.tearDown()
    }

    func testEstadoAcceso_tieneAltasVisibles_enError_cumpleQLT0017() {
        let estadoError = EstadoAccesoBuzon.error(mensaje: "Fallo de conexión en cola")
        XCTAssertTrue(estadoError.tieneAltasVisibles, "QLT-0017: El acceso a buzón debe permanecer visible ante error")
    }

    func testRefrescar_cargaAltasCorrectamente() {
        let action = FixtureComponent2(action: "alta", entityName: "prospecto", status: .pending)
        queue.enqueue(action: action)
        
        sut.refrescar()
        
        XCTAssertEqual(sut.acciones.count, 1)
        XCTAssertEqual(sut.estadoAcceso, .disponible(totalPendientes: 1))
        XCTAssertTrue(sut.estadoAcceso.tieneAltasVisibles)
    }

    func testReintentarAltaEnConflicto_cambiaAFailedAPending() {
        let action = FixtureComponent2(action: "alta", entityName: "prospecto", status: .failed)
        queue.enqueue(action: action)
        sut.refrescar()
        
        XCTAssertEqual(sut.acciones.first?.status, .failed)
        
        sut.reintentarAltaEnConflicto(id: action.id)
        
        let actualizado = queue.loadAll().first(where: { $0.id == action.id })
        XCTAssertEqual(actualizado?.status, .pending)
        XCTAssertEqual(sut.acciones.first?.status, .pending)
    }

    func testReintentarAltaEnConflicto_idInexistente_noAfecta() {
        let action = FixtureComponent2(action: "alta", entityName: "prospecto", status: .pending)
        queue.enqueue(action: action)
        sut.refrescar()
        
        sut.reintentarAltaEnConflicto(id: UUID())
        
        XCTAssertEqual(sut.acciones.count, 1)
        XCTAssertEqual(sut.acciones.first?.status, .pending)
    }
}
