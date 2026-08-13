import cv2 
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os



def stampa_prodotti(result):
    if result.documents:
        for documento in result.documents:

            if documento.fields and "Items" in documento.fields:
                items = documento.fields["Items"]

                print("PRODOTTI TROVATI:")

                for item in items.value:
                    campi_articolo = item.value

                    descrizione = campi_articolo.get("Description")

                    if descrizione:
                        print("-", descrizione.content)

            else:
                print("Nessun prodotto trovato nello scontrino.")
    else:
        print("Nessun documento riconosciuto.")


def main():

    load_dotenv("19-06/.env")

    endpoint = os.getenv("AZ_ENDPOINT")
    key = os.getenv("AZ_KEY")

    if endpoint is None:
        raise ValueError("AZ_ENDPOINT non trovato nel file .env")

    if key is None:
        raise ValueError("AZ_KEY non trovata nel file .env")

    client = DocumentAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Webcam non aperta")
        return

    file_path = "scontrino_salvato.jpeg"

    while True:
        status, frame = cam.read()

        if not status:
            print("Errore nella lettura del fotogramma")
            break
        
        h, w = frame.shape[:2]

        rect_w = 400  
        rect_h = 250

        x = (w - rect_w) // 2
        y = (h - rect_h) // 2

        frame_pulito = frame.copy()

        cv2.rectangle(
            frame,
            (x, y),
            (x + rect_h, y + rect_w),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            "Metti lo scontrino nel riquadro - S salva - Q esci",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.imshow("webcam", frame)

        key = cv2.waitKey(1)

        if key & 0xFF == ord("s"):
            crop = frame_pulito[y:y+rect_h, x:x+rect_w]

            salvato = cv2.imwrite(file_path, crop)

            if salvato:
                print("Scontrino salvato!")
                break
            else:
                print("Errore: scontrino non salvato.")

        if key & 0xFF == ord("q"):
            cam.release()
            cv2.destroyAllWindows()
            return

    cam.release()
    cv2.destroyAllWindows()

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-receipt",
            document=f
        )

    result = poller.result()

    stampa_prodotti(result)


if __name__ == "__main__":
    main()