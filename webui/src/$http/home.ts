import { $http } from '.';

export const createRoleApi = (params: { role_name: string }) => {
  return $http({
    method: 'POST',
    url: '/role/create',
    params,
  });
};

export const getRoleApi = () => {
  return $http({
    method: 'GET',
    url: '/role/',
  });
};

export const deleteRoleApi = (params: { role_name: string }) => {
  return $http({
    method: 'DELETE',
    url: '/role/delete',
    params,
  });
};
