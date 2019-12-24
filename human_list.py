import tkinter
from math import sqrt


class HumanList:
    def __init__(self, window):
        self.list = tkinter.Listbox(window)
        self.list.grid(row=0, column=4)
        # { 213: (x,y,w,h), 390: (x,y,w,h) ...  }
        self.id_face_list = {}
        self.id_index_list = {}

    def update(self, new_faces):
        remain = {}
        still_exist_ids = []
        for (x, y, w, h) in new_faces:
            for _id, (x2, y2, _, _) in self.id_face_list.items():
                if self.d((x, y), (x2, y2)) <= 30:
                    remain[_id] = (x, y, w, h)
                    still_exist_ids.append(self.id((x,y)))

        # まず削除に伴い、IDを更新
        for _id, old_face in self.id_face_list.items():
            if _id not in remain.keys():
                removed_index = self.id_index_list[_id]
                self.list.delete(removed_index)
                del self.id_index_list[_id]
                for __id, id_index in self.id_index_list.items():
                    if id_index > removed_index:
                        self.id_index_list[__id] = id_index - 1

        # 次に、newな奴を挿入していくだけ
        for (x, y, w, h) in new_faces:
            may_be_new_id = self.id((x, y))
            if may_be_new_id not in remain.keys() and may_be_new_id not in still_exist_ids:
                print("here")
                self.list.insert(len(self.id_index_list), "HUMAN1")
                remain[may_be_new_id] = (x, y, w, h)
                self.id_index_list[may_be_new_id] = len(self.id_index_list)

        self.id_face_list = remain

    @staticmethod
    def d(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @staticmethod
    def id(pos):
        x, y = pos
        return x + y
