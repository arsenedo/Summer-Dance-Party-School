from sdps.frontend import Engine
from sdps.backend import DecomposeMp3


def main():
    decompose_mp3 = DecomposeMp3()
    decompose_mp3.run()
    engine = Engine()
    engine.run()

if __name__ == '__main__':
    main()
