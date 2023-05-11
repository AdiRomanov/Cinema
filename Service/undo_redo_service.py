from Domain.undo_redo_operation import UndoRedoOperation


class UndoRedoService:
    def __init__(self):
        self.__undo_operations: list[UndoRedoOperation] = []
        self.__redo_operation:  list[UndoRedoOperation] = []

    def add_undo_operation(self, undo_redo_operation: UndoRedoOperation):
        self.__undo_operations.append(undo_redo_operation)
        self.__redo_operation.clear()

    def undo(self):
        if self.__undo_operations:
            last_undo = self.__undo_operations.pop()
            self.__redo_operation.append(last_undo)
            last_undo.do_undo()

    def redo(self):
        if self.__redo_operation:
            last_redo = self.__redo_operation.pop()
            self.__undo_operations.append(last_redo)
            last_redo.do_redo()
