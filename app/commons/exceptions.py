from fastapi import status, HTTPException


class Exceptions:
    PASSWORDS_NOT_EQUAL = HTTPException(
        detail="Password and Confirm Password must be equal!",
        status_code=status.HTTP_400_BAD_REQUEST
    )
    WRONG_PASSWORD = HTTPException(
        detail="Password is incorrect",
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    WRONG_CREDENTIALS = HTTPException(
        detail="Could not validate credentials",
        status_code=status.HTTP_403_FORBIDDEN,
    )
    USER_IS_NOT_ACTIVE = HTTPException(
        detail="User is not active",
        status_code=status.HTTP_403_FORBIDDEN,
    )
    USER_NOT_FOUND = HTTPException(
        detail="User not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )
    USER_NOT_FOUND_WITH_EMAIl = HTTPException(
        detail="With this email user not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )
    USER_FOUND_WITH_EMAIL = HTTPException(
        detail="With this email already a user found",
        status_code=status.HTTP_409_CONFLICT,
    )


BACK_EXCEPTION = Exceptions()
