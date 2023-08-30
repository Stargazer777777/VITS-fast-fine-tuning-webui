import { FormRules } from 'element-plus/es';

export const rules: FormRules = {
  role_name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 1, max: 20, message: '长度在1-20之间', trigger: 'blur' },
  ],
};
