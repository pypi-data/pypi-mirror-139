from fastapi import Path, Request, HTTPException, status
from typing import Optional, List
from fastapi.security import SecurityScopes
import traceback


class SecurityStructure:
    def __init__(self, scopes: Optional[List[str]] = None, tenants: Optional[List[str]] = None):
        self.scopes = scopes or []
        self.scopes_str = " ".join(self.scopes)
        self.tenants = tenants or []
        self.tenants_str = " ".join(self.tenants)

class VerifySecurity:
    def __init__(self, logger, do_auth):
        self.logger = logger
        self.do_auth = do_auth

    async def verify_security(self, scopes: SecurityScopes, request: Request, tenant_id: str = Path("")): #user_scopes: Optional[str] = Header([], alias="user_scopes")
        try:
            self.logger.info(f'In scopes = {scopes.scopes}, tenants = {tenant_id}')
            security = SecurityStructure(scopes.scopes, [tenant_id])
            if self.do_auth != 'yes':
                return security
            if not request.auth:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorised")
            try:
                user_scopes = request.user.scopes
                user_tenants = request.user.tenants
                self.logger.info(f'User scopes = {user_scopes}, tenants = {user_tenants}')
            except Exception as e:
                self.logger.info(f'Error = {traceback.format_exc()}')
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
            intersection_scopes = list(set(user_scopes) & set(security.scopes))
            if len(intersection_scopes) == 0:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing scopes", )
            intersection_tenants = list(set(user_tenants) & set(security.tenants))
            if len(intersection_tenants) == 0:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing tenants", )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            self.logger.info(f'Error = {traceback.format_exc()}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=traceback.format_exc())
        return SecurityStructure(intersection_scopes, intersection_tenants)
