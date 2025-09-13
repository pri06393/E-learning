from fastapi import Depends, HTTPException, status
from src.auth import get_current_user

def require_instructor(current_user=Depends(get_current_user)):
    if not current_user.instructor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors allowed"
        )
    return current_user

def require_student(current_user=Depends(get_current_user)):
    if not current_user.student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students allowed"
        )
    return current_user

def require_admin(current_user=Depends(get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins allowed"
        )
    return current_user   
    