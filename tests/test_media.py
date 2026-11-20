from nekros.media import media_status


def test_media_integrations_are_reported_as_unconfigured():
    status = media_status()
    assert status["budget"] == "free"
    assert set(status["media_types"]) == {"music", "video", "image", "voice"}
    assert all(not item["available"] for item in status["media_types"].values())
