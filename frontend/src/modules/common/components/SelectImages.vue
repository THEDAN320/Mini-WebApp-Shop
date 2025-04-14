<template>
  <div
    class="grid gap-4"
    :style="{ 'grid-template-columns': `repeat(auto-fill, minmax(130px, 1fr))` }"
  >
    <div
      v-for="image in images"
      :key="image.id"
      @click="toggleSelection(image.id)"
      :class="{
        'border-4 border-blue-500': selectedImages.includes(image.id),
        'cursor-pointer': true,
        'flex items-center justify-center': true,
        'h-32 w-32': true,
        'overflow-hidden': true,
      }"
    >
      <img :src="image.file_path" alt="" class="max-h-full max-w-full" />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, watch, onMounted } from "vue";

export default defineComponent({
  name: "SelectImages",
  props: {
    images: {
      type: Array,
      required: true,
    },
    maxSelection: {
      type: Number,
      default: null,
    },
    initialSelected: {
      type: Array,
      default: () => [],
    },
  },
  setup(props, { emit }) {
    const selectedImages = ref([]);

    const toggleSelection = (id) => {
      if (selectedImages.value.includes(id)) {
        selectedImages.value = selectedImages.value.filter((imgId) => imgId !== id);
      } else {
        if (props.maxSelection === null || selectedImages.value.length < props.maxSelection) {
          selectedImages.value.push(id);
        } else if (selectedImages.value.length >= props.maxSelection) {
          selectedImages.value.shift();
          selectedImages.value.push(id);
        }
      }
      emit("update:selectedImages", selectedImages.value);
    };

    watch(selectedImages, (newVal) => {
      emit("update:selectedImages", newVal);
    });

    const updateSelectedImages = () => {
      if (props.initialSelected.length > 0) {
        selectedImages.value = props.initialSelected.slice(
          0,
          props.maxSelection || props.initialSelected.length,
        );
        emit("update:selectedImages", selectedImages.value);
      }
    };

    onMounted(() => {
      updateSelectedImages();
    });

    watch(
      () => props.initialSelected,
      () => {
        updateSelectedImages();
      },
    );

    return {
      selectedImages,
      toggleSelection,
    };
  },
});
</script>

<style scoped></style>
