<template>
  <div class="space-y-4">
    <n-form
      ref="formRef"
      :model="formValue"
      :rules="rules"
      label-placement="left"
      label-width="160"
      require-mark-placement="right-hanging"
      size="medium"
      @submit.prevent="handleSubmit"
    >
      <n-form-item label="Юзернейм" path="username">
        <n-input v-model:value="formValue.username" placeholder="Введите юзернейм" />
      </n-form-item>

      <n-form-item label="Скидка" path="sale">
        <n-input-number
          v-model:value="formValue.sale"
          :min="0"
          :max="100"
          :precision="2"
          :show-button="false"
          placeholder="Введите скидку"
        />
      </n-form-item>

      <n-form-item label="Телефон" path="phone">
        <n-input v-model:value="formValue.phone" placeholder="Введите телефон" />
      </n-form-item>

      <n-form-item label="Адрес" path="address">
        <n-input v-model:value="formValue.address" placeholder="Введите адрес" />
      </n-form-item>

      <div class="flex justify-end space-x-4">
        <n-button @click="$emit('cancel')">Отмена</n-button>
        <n-button type="primary" attr-type="submit" :loading="loading">
          {{ submitButtonText }}
        </n-button>
      </div>
    </n-form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, defineEmits, watch } from "vue";
import { useStore } from "vuex";
import { NForm, NFormItem, NInput, NInputNumber, NButton, FormInst, FormRules } from "naive-ui";
import { dispatchNotification } from "@/modules/common/utils/notifications";

const props = defineProps<{
  initData?: {
    id?: number;
    username?: string;
    sale?: number;
    phone?: string;
    address?: string;
  };
}>();

const emit = defineEmits<{
  (e: "success"): void;
  (e: "cancel"): void;
}>();

const store = useStore();
const formRef = ref<FormInst | null>(null);
const loading = ref(false);

const formValue = ref({
  username: props.initData?.username || "",
  sale: props.initData?.sale ?? 0,
  phone: props.initData?.phone || "",
  address: props.initData?.address || "",
});

const rules: FormRules = {};

const submitButtonText = computed(() => (props.initData?.id ? "Обновить" : "Создать"));

const handleSubmit = async () => {
  try {
    await formRef.value?.validate();
    loading.value = true;

    const payload = {
      username: formValue.value.username,
      sale: Number(formValue.value.sale),
      phone: formValue.value.phone,
      address: formValue.value.address,
    };

    if (props.initData?.id) {
      // Обновление существующего товара
      const response = await store.dispatch("users/UPDATE_USERS", {
        id: props.initData.id,
        ...payload,
      });
      if (response) {
        dispatchNotification("success", "Успешно", "Пользователь успешно обновлен", true, 3000);
        emit("success");
      }
    } else {
      // Создание нового товара
      const response = await store.dispatch("users/CREATE_USERS", payload);
      if (response) {
        dispatchNotification("success", "Успешно", "Пользователь успешно создан", true, 3000);
        emit("success");
      }
    }
  } catch (error) {
    dispatchNotification(
      "error",
      "Ошибка",
      "Произошла ошибка при сохранении Пользователя",
      true,
      5000,
    );
  } finally {
    loading.value = false;
  }
};
</script>
