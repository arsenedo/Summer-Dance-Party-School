from sdps.backend import DecomposeMp3
from sdps.frontend import Engine


def main():
    decompose_mp3 = DecomposeMp3()
    note_list = decompose_mp3.run()
    engine = Engine(note_list)
    engine.run()

if __name__ == '__main__':
    main()
