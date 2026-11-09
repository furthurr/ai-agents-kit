// Contrato de pruebas anonimizado: nombres sintéticos; no acredita una nueva ejecución del proyecto original.
//
//  OracleSearchProspectsTests.swift
//  FixtureProject Tests
//
//  Oráculo externo para verificar la Tarea 1: GIOS-SEARCH-PROSPECTS
//

import XCTest
@testable import FixtureModule

final class OracleSearchProspectsTests: XCTestCase {

    private var sampleProspectos: [ProspectoItem] = []

    override func setUp() {
        super.setUp()
        sampleProspectos = [
            ProspectoItem(id: "1", nombre: "José María", apellidoPaterno: "Hernández", apellidoMaterno: "López", rfc: "HELJ800101ABC"),
            ProspectoItem(id: "2", nombre: "Carlos", apellidoPaterno: "Álvarez", apellidoMaterno: "Gómez", rfc: "ALGC850505XYZ"),
            ProspectoItem(id: "3", nombre: "María", apellidoPaterno: "Fernández", apellidoMaterno: "Ruiz", rfc: "FERM900909123"),
            ProspectoItem(id: "4", nombre: "Ana", apellidoPaterno: "Hernández", apellidoMaterno: "Álvarez", rfc: "HEAA950101QWE")
        ]
    }

    func testQueryVacio_retornaTodosOrdenados() {
        let useCase = DefaultSearchProspectsUseCase()
        let result = useCase.execute(query: "   ", prospectos: sampleProspectos)
        
        XCTAssertEqual(result.count, 4)
        // Orden alfabético: Álvarez (Carlos), Fernández (María), Hernández (Ana), Hernández (José María)
        XCTAssertEqual(result[0].id, "2") // Álvarez
        XCTAssertEqual(result[1].id, "3") // Fernández
        XCTAssertEqual(result[2].id, "4") // Hernández Álvarez
        XCTAssertEqual(result[3].id, "1") // Hernández López
    }

    func testInsensibilidadAcentosYMayusculas() {
        let useCase = DefaultSearchProspectsUseCase()
        // "jose" sin acento en minúsculas debe encontrar "José María Hernández López"
        let result = useCase.execute(query: "jose", prospectos: sampleProspectos)
        
        XCTAssertEqual(result.count, 1)
        XCTAssertEqual(result.first?.id, "1")
    }

    func testBusquedaPorRfcParcial() {
        let useCase = DefaultSearchProspectsUseCase()
        let result = useCase.execute(query: "900909", prospectos: sampleProspectos)
        
        XCTAssertEqual(result.count, 1)
        XCTAssertEqual(result.first?.id, "3")
    }

    func testBusquedaSinCoincidencias_retornaVacio() {
        let useCase = DefaultSearchProspectsUseCase()
        let result = useCase.execute(query: "ZapatistaInexistente", prospectos: sampleProspectos)
        
        XCTAssertTrue(result.isEmpty)
    }
}
