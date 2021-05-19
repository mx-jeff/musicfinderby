import os, fnmatch

class Music:
    def __init__(self, crawler_name) -> None:
        self.crawler_name = crawler_name

    def find(self,pattern='*.mp3', path='./'):
        print(f"{self.crawler_name} Escaneado música...")
        try:
            result = []
            for root, dirs, files in os.walk(path):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        result.append(os.path.join(root, name))
            
            print(f"{self.crawler_name} {result[0]} Encontrada!")
            return result[0]
        
        except IndexError:
            print(f"{self.crawler_name} Sem músicas encontradas!")
  
    def remove(self):
        music = self.find()
        print(f'{self.crawler_name} Removendo música...')
        if music:
            print(f"{self.crawler_name} Música removida com sucesso!")
            return os.remove(music)
        
        else:
            print(f'{self.crawler_name} Música não existe!')