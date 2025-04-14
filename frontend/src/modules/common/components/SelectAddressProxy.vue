<template>
  <Select
    v-model:value="model.address"
    :options="optionsRef"
    :loading="loadingRef"
    :disabled="disabled"
    :open-on-options-update="selectOpenOnOptionsUpdate"
    @search="handleSearch"
    filterable
  />
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch, PropType } from "vue";
import { useStore } from "vuex";
import Select from "@/modules/common/components/Select.vue";

interface ModelType {
  address: string | null;
}

export default defineComponent({
  name: "AddressSelect",
  components: { Select },
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    value: {
      type: String as PropType<string>,
      default: null,
    },
    defaultCity: {
      type: String,
      default: "",
    },
  },
  setup(props, { emit }) {
    const store = useStore();

    const model = ref<ModelType>({ address: null });
    const loadingRef = ref(false);
    const optionsRef = ref<any[]>([]);
    const selectOpenOnOptionsUpdate = ref(true);
    const lastQuery = ref("");

    const suggestions = computed(() => store.getters["selectAddressProxy/GET_SUGGESTIONS"]);
    const selectedAddress = computed(
      () => store.getters["selectAddressProxy/GET_SELECTED_ADDRESS"],
    );

    const fetchSuggestions = async (term: string) => {
      await store.dispatch("selectAddressProxy/FETCH_SUGGESTIONS", term);
    };
    const fetchSelectedAddress = async (address: string) => {
      await store.dispatch("selectAddressProxy/FETCH_SELECTED_ADDRESS", address);
    };

    const handleSearch = (query: string) => {
      if (!query) {
        optionsRef.value = [];
        return;
      }
      lastQuery.value = query;
      loadingRef.value = true;

      setTimeout(async () => {
        const searchQuery = `${props.defaultCity} ${query}`.trim();
        await fetchSuggestions(searchQuery);

        optionsRef.value = suggestions.value.map((item: any) => ({
          label: item.value,
          value: item.unrestricted_value,
        }));
        loadingRef.value = false;
      }, 500);
    };

    watch(
      () => props.value,
      (newVal) => {
        model.value.address = newVal;
      },
      { immediate: true },
    );

    let internalChange = false;
    watch(
      () => model.value.address,
      async (newVal) => {
        if (internalChange) {
          internalChange = false;
          return;
        }
        if (newVal) {
          const suggestion = suggestions.value.find(
            (item: any) => item.unrestricted_value === newVal,
          );
          if (suggestion) {
            await fetchSelectedAddress(suggestion.unrestricted_value);
            const geoData = selectedAddress.value;
            if (geoData) {
              const result = {
                long_name: geoData.value,
                short_name: suggestion.value,
                latitude: geoData.latitude,
                longitude: geoData.longitude,
                house: geoData.house,
                entrance: geoData.entrance,
                floor: geoData.floor,
                flat: geoData.flat,
              };
              emit("update:data", result);
              emit("update:dataAll", { ...geoData, suggestion });
              emit("update:value", suggestion.unrestricted_value);
            }
          }
        } else {
          emit("update:data", null);
          emit("update:dataAll", null);
          emit("update:value", null);
        }
      },
    );

    watch(
      () => props.defaultCity,
      () => {
        handleSearch(lastQuery.value);
      },
    );

    return {
      model,
      loadingRef,
      optionsRef,
      handleSearch,
      selectOpenOnOptionsUpdate,
    };
  },
});
</script>

<style scoped></style>
