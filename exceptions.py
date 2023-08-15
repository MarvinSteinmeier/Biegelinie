class GeneralUserError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
    
    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv

class NoElementsInSystemError(GeneralUserError):
    def __init__(self, 
                 message="Erstellen Sie bitte ein System bestehend aus Balken und Lagern bevor Sie auf 'System berechnen' klicken!", 
                 status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class NoValidBondsInSystemError(GeneralUserError):
    def __init__(self,message="Sie müssen für alle eingefügten Balken auch einen passenden Systemrand oder -übergang einfügen.",
                 status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class BondsAtPositionError(GeneralUserError):
    def __init__(self,
                 message="An einer Position darf nur ein Symbol für einen Systemrand oder -übergang sitzen.",
                 status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class ToLessBeamsAtMatchingConditionPositionError(GeneralUserError):
    def __init__(self,
                 message="Übergangselemente müssen an ihren beiden Enden jeweils mit einem Balken verbunden sein.",
                 status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class RigidBeamEndsInNothingError(GeneralUserError):
    def __init__(self,
                 message="An einem starren Balkenteil muss etwas an beiden Enden angreifen.",
                 status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class TorsionalSpringAtJointError(GeneralUserError):
    def __init__(self, message, status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class JointAndFreeEndConfusionError(GeneralUserError):
    def __init__(self, message, status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class DegreeOfIndeterminacyError(GeneralUserError):
    def __init__(self,
                 message="Das eingegebene System ist statisch unterbestimmt (n_s<0). Eine Berechnung ist nicht zielführend.",
                 status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()