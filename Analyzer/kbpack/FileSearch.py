import os

class Search():
    # 파일 검색 (폴더명 혹은 전체탐색 시 .)
    # 현재 경로 확인 필수
    def data_search(self, dirname, filetype='.json'):
        filenames = os.listdir(dirname)
        fl = []
        for filename in filenames:
            if filetype in filename:
                fl.append(os.path.join(dirname, filename))
        
        return fl
