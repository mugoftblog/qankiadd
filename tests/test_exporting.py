from exporting.anki import *
import shutil
import msvcrt
import time

field1 = FieldModel(None)
field1.set_text("Question")

field2 = FieldModel(None)
field2.set_text("Answer")

fields = [field1, field2]


def __clean_output_dir():
    # try to remove the output directory with all files inside
    if os.path.exists(OUTPUT_DIR):
        print("Deleting output directory")
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
        t = 0
        # wait max 5 seconds until directory is deleted
        while os.path.exists(OUTPUT_DIR) and t < 5:  # check if it exists
            t += 0.5
            time.sleep(0.5)


def __create_output_dir():
    # create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        print("Creating output directory")
        os.makedirs(OUTPUT_DIR)


def test_exporting_dir_dontexist():
    """
    Procedure:
        - remove output directory
        - write text of the fields via ankiexporter
    Explanation:
        during writing text of the fields ankiexporter should detect that
        output directory doesn't exist anymore and create new output directory
    Expectation:
        - output directory is created
        - ankiexporter successfully writes text from the fields into the file
    """
    __clean_output_dir()

    anki = AnkiExporter()

    anki.write(fields)

    f = open(anki._path, 'r')
    assert f.readline() != ""
    f.close()


def test_exporting_write():
    """
    Procedure:
        - clean output directory
        - write text of the fields via ankiexporter
        - write text of the fields via ankiexporter again
    Explanation:
         After first call of the "write" method of the ankiexporter
         it creates new directory, new ankifile and writes one line of the text into
         this file.
         After second call of the "write" method, ankieporter detects ankifile,
         opens it and write one line of the text into this file
    Expectation:
        - output directory is created
        - one ankifile is created and contains two line of text
    """
    __clean_output_dir()
    __create_output_dir()

    """create only one file even though few writes are done"""
    anki = AnkiExporter()
    anki.write(fields)

    f = open(anki._path, 'r')
    assert f.readline() != ""
    f.close()

    # write second line to the same file
    anki.write(fields)

    f = open(anki._path, 'r')
    assert f.readline() != ""
    assert f.readline() != ""
    f.close()


def test_exporting_file_cantbe_closed():
    """
    Procedure:
        - create anki file and lock it
        - write text of the fields via ankiexporter into anki file
        (ankiexporter will try to write the text into the locked file)
    Explanation:
        After we force ankiexporter write text of the fields,
        it detects that ankifile already exists and opens it for writing.
        Then ankiexporter execute "write" command for the open file
        and tries to close it. But during closing the file
        "permission denied" error occurs as the file is locked.
    Expectation:
        - permission denied error occured and written to the
        log file.
        - anki file will contain only dummy text as writing of the fields text
        was not accomplished
        - text from the fields is written into the log file
        to make possible to restore it later.
        - program is exited (sys.exit(0))
    """
    __clean_output_dir()
    __create_output_dir()

    anki = AnkiExporter()
    old_path = anki.get_path()
    f = open(old_path, 'ab')
    f.write("dummy_text".encode("utf-8"))

    # lock file so that it couldn't be closed
    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 10)
    # anki exporter is trying to write something but error occured during closing the file

    anki.write(fields)
    # unlock and close the file for clean stop
    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 10)
    f.close()

    # but in the file created by anki we expect to see something
    f = open(old_path, 'r')
    assert f.readline() == "dummy_text"
    f.close()


def test_exporting_write_many_lines():
    """
        Procedure:
            - write text of the fields via ankiexporter until ankifile becomes bigger
            than maximum allowed size
        Explanation:
            If the size of ankifile becomes bigger that maximum allowed size
            ankiexporter detects it and creates another ankifile
        Expectation:
            two ankifiles are expected:
            - first one has the size approximately equal to the maximum allowed size
            - second one is created and maybe contains some text
        """
    __clean_output_dir()
    __create_output_dir()

    """create only one file even though few writes are done"""
    anki = AnkiExporter()
    anki.write(fields)

    f = open(anki.get_path(), 'r')
    assert f.readline() != ""
    f.close()

    old_path = anki.get_path()

    text_fields_size = 0
    for field in fields:
        text_fields_size += len(field.get_text())

    # write second line to the same file
    file_size_approx = 0

    while file_size_approx < anki._size_max:
        anki.write(fields)
        file_size_approx += text_fields_size

    assert old_path != anki.get_path(), "at least two files are expected after so many writes"

    statinfo = os.stat(old_path)

    # assume that size of the symbols for anki format is not bigger than 100 byte
    symbols_format_size = 100
    assert statinfo.st_size < anki._size_max + text_fields_size + symbols_format_size, "size of the first file should be less than max allowed size + size of the last written line"


test_exporting_dir_dontexist()
test_exporting_write()
test_exporting_file_cantbe_closed()
test_exporting_write_many_lines()