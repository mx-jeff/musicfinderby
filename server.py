from src.app import handleMusic
from src.utils import tempo_estimado, timeit

def main():
    handleMusic()


if __name__ == "__main__":
    start = timeit.default_timer()
    
    try:
        main()

        tempo_estimado(start)

    except KeyboardInterrupt:
        tempo_estimado(start)
