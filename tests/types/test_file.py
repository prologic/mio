def test_repr(mio):
    file = mio.eval("File")
    assert repr(file) == "<type 'File'>"


def test_repr2(mio, tmpdir):
    filename = str(tmpdir.ensure("test.txt"))
    mode = "r"

    file = mio.eval("File open(\"%s\", \"r\")" % filename)
    assert repr(file) == "<open File {0:s}, mode={1:s} at {2:s}>".format(repr(filename), repr(mode), hex(id(file)))


def test_open(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    file = mio.eval("File open(\"%s\", \"r\")" % filename)
    assert file.value.name == filename
    assert file.value.closed is False
    assert file.value.mode == "r"


def test_open_status(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    mio.eval("f = File open(\"%s\", \"r\")" % filename)
    assert mio.eval("f filename") == filename
    assert mio.eval("f closed").value is False
    assert mio.eval("f mode") == "r"


def test_close(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    mio.eval("f = File open(\"%s\", \"r\")" % filename)
    f = mio.eval("f")
    assert f.value.name == filename
    assert f.value.closed is False
    assert f.value.mode == "r"

    mio.eval("f close")
    assert f.value.closed is True


def test_closed_status(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    mio.eval("f = File open(\"%s\", \"r\")" % filename)
    assert mio.eval("f filename") == filename
    assert mio.eval("f closed").value is False
    assert mio.eval("f mode") == "r"

    mio.eval("f close")
    assert mio.eval("f closed").value is True


def test_read(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = "Hello World!"
    filename.open("w").write(data)

    assert mio.eval("File open(\"%s\", \"r\") read" % filename) == data


def test_read_limited(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = "Hello World!"
    filename.open("w").write(data)

    assert mio.eval("File open(\"%s\", \"r\") read(5)" % filename) == data[:5]


def test_readline(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = "Hello World!\nGoodbye World!"
    filename.open("w").write(data)

    mio.eval("f = File open(\"%s\", \"r\")" % filename)
    s = mio.eval("f readline")
    assert s == "Hello World!\n"


def test_write(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = "Hello World!"
    mio.eval("File open(\"%s\", \"w\") write(\"%s\")" % (filename, data))

    assert mio.eval("File open(\"%s\", \"r\") read" % filename) == data


def test_readlines(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = ["Hello World!", "Goodbye World!"]
    filename.open("w").writelines(data)

    s = ["".join(data)]
    assert mio.eval("File open(\"%s\", \"r\") readlines" % filename) == s


def test_writelines(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = ["Hello World!", "Goodbye World!"]
    mio.eval("lines = List clone")
    for x in data:
        mio.eval("lines append(\"%s\")" % x)

    mio.eval("f = File open(\"%s\", \"w\")" % filename)
    mio.eval("f writelines(lines)")
    mio.eval("f close")

    s = ["".join(data)]
    assert filename.open("r").readlines() == s
    assert mio.eval("File open(\"%s\", \"r\") readlines" % filename) == s


def test_iter(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = "Hello World!"
    filename.open("w").write(data)

    file = mio.eval("File open(\"%s\", \"r\")" % filename)
    assert list(iter(file)) == [data]


def test_pos(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = "Hello World!"
    filename.open("w").write(data)

    mio.eval("f = File open(\"%s\", \"r\")" % filename)
    mio.eval("f read(1)")
    assert mio.eval("f pos") == 1


def test_seek(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = "Hello World!"
    filename.open("w").write(data)

    mio.eval("f = File open(\"%s\", \"r\")" % filename)
    mio.eval("f read") == data

    mio.eval("f seek(0)")
    mio.eval("f read") == data


def test_truncate(mio, tmpdir):
    tmpdir.ensure("test.txt")
    filename = tmpdir.join("test.txt")

    data = "Hello World!"
    filename.open("w").write(data)

    mio.eval("f = File open(\"%s\", \"w+\")" % filename)
    mio.eval("f read") == data

    mio.eval("f truncate")
    mio.eval("f seek(0)")
    mio.eval("f read") == ""
