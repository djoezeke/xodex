import os
import pickle

import pytest

from xodex.game.storage import Storage


# Dummy serializer/deserializer mixins for testing
class DummyStorage(Storage):
    def __init__(self):
        super().__init__()
        self.value = 0
        self.filename = "testfile"

    def serialize(self):
        return {"value": self.value}

    def deserialize(self, data):
        self.value = data.get("value", 0)

    def serialize_binary(self):
        return pickle.dumps({"value": self.value})

    def deserialize_binary(self, data):
        obj = pickle.loads(data)
        self.value = obj.get("value", 0)


@pytest.fixture
def temp_storage_dir(tmp_path):
    orig_path = Storage.data_path
    Storage.data_path = str(tmp_path)
    yield tmp_path
    Storage.data_path = orig_path


def test_json_save_and_load(temp_storage_dir):
    s = DummyStorage()
    s.value = 42
    s.binary = False
    s.save()
    s.value = 0
    s.load()
    assert s.value == 42
    # File should exist
    path = os.path.join(
        Storage.data_path,
        s.filename + ".jxox" if not s.filename.endswith(".jxox") else s.filename,
    )
    assert os.path.exists(path) or os.path.exists(os.path.join(Storage.data_path, s.filename))


def test_binary_save_and_load(temp_storage_dir):
    s = DummyStorage()
    s.value = 99
    s.binary = True
    s.save()
    s.value = 0
    s.load()
    assert s.value == 99
    # File should exist
    path = os.path.join(
        Storage.data_path,
        s.filename + ".bxox" if not s.filename.endswith(".bxox") else s.filename,
    )
    assert os.path.exists(path) or os.path.exists(os.path.join(Storage.data_path, s.filename))


def test_load_missing_creates_file(temp_storage_dir):
    s = DummyStorage()
    s.value = 123
    s.binary = False
    # Remove file if exists
    path = os.path.join(Storage.data_path, s.filename + ".jxox")
    if os.path.exists(path):
        os.remove(path)
    s.load()
    # Should create file
    assert os.path.exists(path) or os.path.exists(os.path.join(Storage.data_path, s.filename))


def test_event_handler_stub():
    s = DummyStorage()
    assert s.event_handler("event") is None


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
