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
      <n-form-item label="Название" path="name">
        <n-input v-model:value="formValue.name" placeholder="Введите название товара" />
      </n-form-item>

      <n-form-item label="Артикул" path="article">
        <n-input v-model:value="formValue.article" placeholder="Введите артикул" />
      </n-form-item>

      <n-form-item label="Цена" path="price">
        <n-input-number
          v-model:value="formValue.price"
          :min="0"
          :precision="2"
          :show-button="false"
          placeholder="Введите цену"
        />
      </n-form-item>

      <n-form-item label="Количество" path="count">
        <n-input-number
          v-model:value="formValue.count"
          :min="0"
          :precision="0"
          :show-button="false"
          placeholder="Введите количество"
        />
      </n-form-item>

      <n-form-item label="Тип" path="type">
        <n-input v-model:value="formValue.type" placeholder="Введите тип товара" />
      </n-form-item>

      <n-form-item label="URL изображения" path="url">
        <n-input v-model:value="formValue.url" placeholder="Введите URL изображения" />
      </n-form-item>

      <n-form-item label="Описание" path="description">
        <n-input
          v-model:value="formValue.description"
          type="textarea"
          placeholder="Введите описание товара"
        />
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
    name?: string;
    article?: string;
    price?: number;
    count?: number;
    type?: string;
    url?: string;
    description?: string;
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
  name: props.initData?.name || "",
  article: props.initData?.article || "",
  price: props.initData?.price ?? 0,
  count: props.initData?.count ?? 0,
  type: props.initData?.type || "",
  url: props.initData?.url || "",
  description: props.initData?.description || "",
});

const rules: FormRules = {
  name: {
    required: true,
    message: "Введите название товара",
    trigger: ["blur", "input"],
  },
  article: {
    required: true,
    message: "Введите артикул",
    trigger: ["blur", "input"],
  },
  type: {
    required: true,
    message: "Введите тип товара",
    trigger: ["blur", "input"],
  },
};

const submitButtonText = computed(() => (props.initData?.id ? "Обновить" : "Создать"));

const handleSubmit = async () => {
  try {
    await formRef.value?.validate();
    loading.value = true;

    const payload = {
      name: formValue.value.name,
      article: formValue.value.article,
      price: Number(formValue.value.price),
      count: Number(formValue.value.count),
      type: formValue.value.type,
      url: formValue.value.url,
      description: formValue.value.description,
    };

    if (props.initData?.id) {
      // Обновление существующего товара
      const response = await store.dispatch("goods/UPDATE_GOODS", {
        id: props.initData.id,
        ...payload,
      });
      if (response) {
        dispatchNotification("success", "Успешно", "Товар успешно обновлен", true, 3000);
        emit("success");
      }
    } else {
      // Создание нового товара
      const response = await store.dispatch("goods/CREATE_GOODS", payload);
      if (response) {
        dispatchNotification("success", "Успешно", "Товар успешно создан", true, 3000);
        emit("success");
      }
    }
  } catch (error) {
    dispatchNotification("error", "Ошибка", "Произошла ошибка при сохранении товара", true, 5000);
  } finally {
    loading.value = false;
  }
};
</script>
