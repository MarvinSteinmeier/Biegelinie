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
    def __init__(self, message, status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class NoValidBondsInSystemError(GeneralUserError):
    def __init__(self, message, status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class BondsAtPositionError(GeneralUserError):
    def __init__(self, message, status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class ToLessBeamsAtMatchingConditionPositionError(GeneralUserError):
    def __init__(self, message, status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()

class RigidBeamEndsInNothingError(GeneralUserError):
    def __init__(self, message, status_code=None):
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
    def __init__(self, message, status_code=None):
        super().__init__(message, status_code)
    
    def to_dict(self):
        return super().to_dict()