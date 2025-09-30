from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from app.config import settings

client = ImageAnalysisClient(settings.vision_endpoint, AzureKeyCredential(settings.vision_key))

def extract_text_from_image(image_bytes: bytes) -> str:
    """Use Azure Vision OCR to extract text from an uploaded image."""
    result = client.analyze(image_data=image_bytes, visual_features=[])
    if not getattr(result, "read", None):
        return ""
    lines = []
    for block in result.read.blocks:
        for line in block.lines:
            words = [w.text for w in line.words]
            lines.append(" ".join(words))
    return "\n".join(lines)
