from fastapi.testclient import TestClient

from main import app

cliente = TestClient(app)


def test_recomendaciones_de_afiliado_existente():
    respuesta = cliente.get("/afiliados/AF-000001/recomendaciones")
    assert respuesta.status_code == 200

    cuerpo = respuesta.json()
    assert cuerpo["id_afiliado"] == "AF-000001"
    assert isinstance(cuerpo["recomendaciones"], list)
    if cuerpo["recomendaciones"]:
        primera = cuerpo["recomendaciones"][0]
        assert {"producto", "puntaje", "razones"} <= primera.keys()


def test_afiliado_inexistente_devuelve_404():
    respuesta = cliente.get("/afiliados/AF-999999/recomendaciones")
    assert respuesta.status_code == 404


def test_lote_con_csv_en_memoria():
    contenido_csv = b"ID Afiliado\nAF-000001\nAF-000002\nAF-999999\n"
    archivo = ("afiliados.csv", contenido_csv, "text/csv")

    respuesta = cliente.post(
        "/afiliados/recomendaciones/lote", files={"archivo": archivo}
    )
    assert respuesta.status_code == 200

    cuerpo = respuesta.json()
    ids_encontrados = {resultado["id_afiliado"] for resultado in cuerpo["resultados"]}
    assert ids_encontrados == {"AF-000001", "AF-000002"}
    assert cuerpo["ids_no_encontrados"] == ["AF-999999"]
