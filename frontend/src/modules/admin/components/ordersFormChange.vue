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
      <n-form-item label="Цена" path="price">
        <n-input-number
          v-model:value="formValue.price"
          :min="0"
          :precision="2"
          :show-button="false"
          placeholder="Введите цену"
        />
      </n-form-item>

      <n-form-item label="Скидка" path="sale">
        <n-input-number
          v-model:value="formValue.sale"
          :min="0"
          :precision="0"
          :show-button="false"
          placeholder="Введите скидку"
        />
      </n-form-item>

      <n-form-item label="Статус оплаты" path="is_paid">
        <n-space>
          <n-switch v-model:value="formValue.is_paid" size="medium" />
        </n-space>
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
import { NForm, NFormItem, NSwitch, NInputNumber, NButton, FormInst, FormRules } from "naive-ui";
import { dispatchNotification } from "@/modules/common/utils/notifications";

const props = defineProps<{
  initData?: {
    id?: number;
    price?: number;
    sale?: number;
    is_paid?: boolean;
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
  price: props.initData?.price ?? 0,
  sale: props.initData?.sale ?? 0,
  is_paid: props.initData?.is_paid || false,
});

const rules: FormRules = {};

const submitButtonText = computed(() => (props.initData?.id ? "Обновить" : "Создать"));

const handleSubmit = async () => {
  try {
    await formRef.value?.validate();
    loading.value = true;

    const payload = {
      price: Number(formValue.value.price),
      sale: Number(formValue.value.sale),
      is_paid: formValue.value.is_paid,
    };

    if (props.initData?.id) {
      const response = await store.dispatch("orders/UPDATE_ORDERS", {
        id: props.initData.id,
        ...payload,
      });
      if (response) {
        dispatchNotification("success", "Успешно", "Заказ успешно обновлен", true, 3000);
        emit("success");
      }
    } else {
      const response = await store.dispatch("orders/CREATE_ORDERS", payload);
      if (response) {
        dispatchNotification("success", "Успешно", "Заказ успешно создан", true, 3000);
        emit("success");
      }
    }
  } catch (error) {
    dispatchNotification("error", "Ошибка", "Произошла ошибка при сохранении заказа", true, 5000);
  } finally {
    loading.value = false;
  }
};
</script>
