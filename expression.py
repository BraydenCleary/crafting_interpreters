from abc import ABC

class Expr(ABC):
    def __init__(self):
        pass

    def accept(self, visitor):
        pass
    
class ExprVisitor(ABC):
    
    def visitBinaryExpr(self, expr_instance):
        pass

        
    def visitGroupingExpr(self, expr_instance):
        pass

        
    def visitLiteralExpr(self, expr_instance):
        pass

        
    def visitUnaryExpr(self, expr_instance):
        pass

        
class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)
        
class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)
        
class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)
        
class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)