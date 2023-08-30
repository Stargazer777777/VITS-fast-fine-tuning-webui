<template>
  <div class="container">
    <div class="welcome">欢迎使用 VITS FAST AI VOICE</div>
    <div class="list">
      <div class="item card" @click="open">
        <i class="iconfont icon-user"></i>
        <span class="title">创建角色</span>
        <div class="desc">通过创建角色为你训练的声音标识,仅支持英文字母</div>
      </div>
      <div class="item card" @click="getRole">
        <i class="iconfont icon-view"></i>
        <span class="title">查看角色</span>
        <div class="desc">查看历史训练的声音数据</div>
      </div>
    </div>
    <div class="role-list card" v-if="roleList.length">
      <div class="role-item card" v-for="(item, index) in roleList" :key="item">
        <el-popconfirm
          width="220"
          confirm-button-text="确定"
          cancel-button-text="取消"
          icon-color="#ffc83e"
          title="你确定要删除这个声音吗？"
          @confirm="deleteRole(item)"
        >
          <template #reference>
            <i class="iconfont icon-cuowu" @click.stop></i>
          </template>
        </el-popconfirm>
        <el-avatar :src="imgs[index % 20]" />
        <span class="name">{{ item }}</span>
      </div>
    </div>
    <el-dialog v-model="dialogFormVisible" title="创建角色" width="400px">
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item label="角色名称" prop="role_name">
          <el-input v-model="form.role_name" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="btns">
          <div class="btn default" @click="dialogFormVisible = false">取消</div>
          <div class="btn" @click="createRole">创建</div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { createRoleApi, getRoleApi, deleteRoleApi } from '@/$http/home';
import { ElMessage, FormInstance } from 'element-plus/es';
import { ref } from 'vue';
import { rules } from '@/rules/role.rule';
import router from '@/router';

const imgs = ref<string[]>([]);

const getImgs = async () => {
  for (let i = 1; i <= 20; i++) {
    let res = await import(`../assets/img/${i}.jpg`);
    imgs.value.push(res.default);
  }
};
getImgs();

const form = ref({
  role_name: '',
});
const roleList = ref<string[]>([]);
const formRef = ref<FormInstance>();
const dialogFormVisible = ref(false);
const createRole = async () => {
  await formRef.value?.validate();
  const res = await createRoleApi(form.value);
  console.log(res);
  ElMessage.success('创建角色成功！');
  dialogFormVisible.value = false;
  formRef.value?.resetFields();
  // getRole();
  router.push('/train');
};
const open = () => {
  dialogFormVisible.value = true;
};

const getRole = async () => {
  const res = await getRoleApi();
  roleList.value = res.data;
  if (!roleList.value.length) {
    ElMessage.error('你还没有创建任何角色噢~');
  }
};
const deleteRole = async (name: string) => {
  await deleteRoleApi({ role_name: name });
  ElMessage.success('删除角色成功！');
  getRole();
};
</script>

<style scoped lang="scss">
.container {
  min-width: 636px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ffc83e;
  .welcome {
    margin-top: 100px;
    font-weight: 600;
    font-size: 40px;
  }
  .list {
    margin-top: 50px;
    width: 80%;
    height: 500px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .item {
      width: 40%;
      height: 300px;
      padding: 40px;
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      .iconfont {
        font-size: 60px;
        margin-bottom: 20px;
      }
      .icon-view {
        font-size: 54px;
      }
      .title {
        font-weight: 600;
        font-size: 20px;
        margin-bottom: 30px;
      }
      .desc {
        color: #4f3d11;
        font-weight: 600;
      }
    }
  }

  :deep(.el-dialog) {
    border-radius: 20px;
  }
  .el-input {
    :deep(.el-input__wrapper) {
      border-radius: 20px;
    }
    :deep(.is-focus) {
      box-shadow: 0 0 1px #ffc83e inset;
    }
  }
  .default {
    background-color: #fff;
    border: 1px solid #ffc83e;
  }
  .role-list {
    width: 80%;
    padding: 20px;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-column-gap: 10px;
    grid-row-gap: 10px;
    margin-bottom: 50px;
    .role-item {
      cursor: pointer;
      padding: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      .name {
        margin-top: 10px;
      }
      .icon-cuowu {
        font-size: 26px;
        position: absolute;
        top: 5px;
        right: 5px;
        opacity: 0;
        transition: all 0.5s;
      }
      &:hover .icon-cuowu {
        opacity: 100;
      }
    }
  }
}
</style>
