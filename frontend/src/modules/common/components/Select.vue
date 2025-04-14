<template>
  <div class="relative w-full">
    <div
      ref="trigger"
      class="btn-select relative min-h-[34px] w-full rounded bg-white pr-6 pt-1 text-left text-gray-900 ring-1 ring-inset ring-gray-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm sm:leading-6"
      aria-haspopup="true"
      @click.stop="toggleDropdownOpen"
      :aria-expanded="dropdownOpen"
    >
      <div class="relative flex w-full flex-wrap items-center">
        <div v-if="showPlaceholder" class="placeholder">
          <div class="placeholder__inner">{{ placeholder }}</div>
        </div>

        <template v-if="showSelectedOptions">
          <div v-for="item in selectedOptions" :key="item.value" class="max-w-full pb-1 pl-1">
            <div class="flex items-center justify-center rounded bg-gray-100 pl-1">
              <span class="ml-1 block">{{ item.label }}</span>

              <div
                tabindex="-1"
                aria-disabled="false"
                aria-label="close"
                role="button"
                disabled="false"
                class="relative mx-[4px] flex cursor-pointer items-center justify-center rounded p-[2px] outline-none transition duration-300 ease-in-out hover:bg-gray-300"
                @click.stop="closeTagOption(item)"
              >
                <i class="relative inline-block h-[14px] w-[14px] text-center">
                  <svg
                    viewBox="0 0 12 12"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                  >
                    <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                      <g fill="currentColor" fill-rule="nonzero">
                        <path
                          d="M2.08859116,2.2156945 L2.14644661,2.14644661 C2.32001296,1.97288026 2.58943736,1.95359511 2.7843055,2.08859116 L2.85355339,2.14644661 L6,5.293 L9.14644661,2.14644661 C9.34170876,1.95118446 9.65829124,1.95118446 9.85355339,2.14644661 C10.0488155,2.34170876 10.0488155,2.65829124 9.85355339,2.85355339 L6.707,6 L9.85355339,9.14644661 C10.0271197,9.32001296 10.0464049,9.58943736 9.91140884,9.7843055 L9.85355339,9.85355339 C9.67998704,10.0271197 9.41056264,10.0464049 9.2156945,9.91140884 L9.14644661,9.85355339 L6,6.707 L2.85355339,9.85355339 C2.65829124,10.0488155 2.34170876,10.0488155 2.14644661,9.85355339 C1.95118446,9.65829124 1.95118446,9.34170876 2.14644661,9.14644661 L5.293,6 L2.14644661,2.85355339 C1.97288026,2.67998704 1.95359511,2.41056264 2.08859116,2.2156945 L2.14644661,2.14644661 L2.08859116,2.2156945 Z"
                        ></path>
                      </g>
                    </g>
                  </svg>
                </i>
              </div>
            </div>
          </div>
        </template>

        <div v-if="filterable" class="selection-input">
          <textarea
            :key="keyTextarea"
            ref="textarea"
            class="selection-input__input"
            :class="{ 'cursor-not-allowed': disabled }"
            :disabled="disabled"
            type="text"
            rows="1"
            v-model="inputValue"
            @input="changeTextareaRows"
          />
        </div>
      </div>

      <span
        class="pointer-events-none absolute inset-y-0 right-0 ml-2 flex items-center pr-2"
        :class="{ 'chevron-down': selectedOptions.length > 0 }"
      >
        <svg
          class="h-4 w-4 text-gray-300"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 512 512"
        >
          <path
            fill="none"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="48"
            d="M112 184l144 144l144-144"
          ></path>
        </svg>
      </span>

      <span
        v-if="showClearSelectedOptions && !disabled"
        class="close-circle absolute inset-y-0 right-0 ml-2 hidden cursor-pointer items-center pr-2"
        @click.stop="clearSelectedOptions"
      >
        <svg
          class="h-4 w-4 text-gray-300"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 0 512 512"
        >
          <path
            d="M256 48C141.31 48 48 141.31 48 256s93.31 208 208 208s208-93.31 208-208S370.69 48 256 48zm75.31 260.69a16 16 0 1 1-22.62 22.62L256 278.63l-52.69 52.68a16 16 0 0 1-22.62-22.62L233.37 256l-52.68-52.69a16 16 0 0 1 22.62-22.62L256 233.37l52.69-52.68a16 16 0 0 1 22.62 22.62L278.63 256z"
            fill="currentColor"
          ></path>
        </svg>
      </span>

      <div v-if="loading" class="wrap-loader">
        <span class="loader"></span>
      </div>
    </div>

    <div
      v-if="dropdownOpen && options.length > 0"
      class="absolute z-10 mt-1 max-h-56 min-h-[42px] w-full overflow-auto rounded-md bg-white p-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
    >
      <ul ref="dropdown" @focusin="dropdownOpen = true" @focusout="dropdownOpen = false">
        <li
          v-for="item in options"
          :key="item.value"
          class="relative cursor-default select-none text-gray-900"
          id="listbox-option-0"
          role="option"
          @click.stop="clickOnOption(item)"
        >
          <div class="rounded px-1 py-1.5 hover:cursor-pointer hover:bg-gray-100">
            <div class="flex items-center">
              <span
                class="ml-1 block w-[96%] font-normal"
                :class="{
                  'text-indigo-600': selectedOptions.find(
                    (element) => element.value === item.value,
                  ),
                }"
                style="white-space: pre-line"
              >
                {{ item.label }}
              </span>
            </div>

            <span
              class="absolute inset-y-0 right-0 flex items-center pr-1 text-indigo-600"
              :class="{
                invisible: !selectedOptions.find((element) => element.value === item.value),
              }"
            >
              <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path
                  fill-rule="evenodd"
                  d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z"
                  clip-rule="evenodd"
                />
              </svg>
            </span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import {
  ref,
  onMounted,
  onUnmounted,
  defineComponent,
  PropType,
  watch,
  computed,
  nextTick,
} from "vue";

interface OptionType {
  value: any;
  label: any;
}

export default defineComponent({
  components: {},
  name: "SelectView",
  props: {
    options: {
      type: Array as PropType<OptionType[]>,
      default: () => [],
    },
    value: {
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    filterable: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: "Введите",
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    openOnOptionsUpdate: {
      type: Boolean,
      default: true,
    },
  },

  setup(props, context) {
    const dropdownOpen = ref(false);
    const trigger = ref();
    const dropdown = ref();
    const selectedOptions = ref<OptionType[]>([]);

    const textarea = ref();
    const keyTextarea = ref(Math.random());
    const inputValue = ref<any>("");

    const showPlaceholder = ref(true);
    let selectedOptionValuesForResult: Array<number> = [];
    const resultValue = ref<any | Array<any> | undefined>(null);

    const toggleDropdownOpen = () => {
      dropdownOpen.value = !dropdownOpen.value;
    };

    // close on click outside
    const clickHandler = ({ target }: { target: any }) => {
      if (
        !dropdownOpen.value ||
        (dropdown.value && dropdown.value.contains(target)) ||
        (dropdown.value && trigger.value.contains(target))
      )
        return;
      dropdownOpen.value = false;
    };

    // close if the esc key is pressed
    const keyHandler = ({ keyCode }: { keyCode: number }) => {
      if (!dropdownOpen.value || keyCode !== 27) return;
      dropdownOpen.value = false;
    };

    onMounted(() => {
      document.addEventListener("click", clickHandler);
      document.addEventListener("keydown", keyHandler);
    });

    onUnmounted(() => {
      document.removeEventListener("click", clickHandler);
      document.removeEventListener("keydown", keyHandler);
    });

    const clearSelectedOptions = () => {
      selectedOptions.value = [];
      selectedOptionValuesForResult = [];
      inputValue.value = "";
      resultValue.value = [...selectedOptionValuesForResult];
    };

    const removeOptionByValue = (arr: OptionType[], value: any) => {
      return arr.filter((obj: OptionType) => obj.value !== value);
    };

    const clickOnOption = (item: OptionType) => {
      if (!selectedOptions.value.find((element) => element.value === item.value)) {
        if (props.multiple) {
          selectedOptions.value.push({ value: item.value, label: item.label });
          selectedOptionValuesForResult.push(item.value);
        } else {
          selectedOptions.value = [{ value: item.value, label: item.label }];
          selectedOptionValuesForResult = [item.value];
          dropdownOpen.value = false;

          if (props.filterable) {
            inputValue.value = item.label;
            nextTick(() => {
              inputValue.value = "";
              inputValue.value = item.label;
            });
          } else {
            inputValue.value = "";
          }
        }
      } else {
        selectedOptions.value = removeOptionByValue(selectedOptions.value, item.value);
        selectedOptionValuesForResult = selectedOptionValuesForResult.filter(
          (value: any) => value !== item.value,
        );
      }
      resultValue.value = [...selectedOptionValuesForResult];
    };

    const closeTagOption = (item: any) => {
      selectedOptions.value = removeOptionByValue(selectedOptions.value, item.value);
      selectedOptionValuesForResult = selectedOptionValuesForResult.filter(
        (value: any) => value !== item.value,
      );
      resultValue.value = [...selectedOptionValuesForResult];
    };

    const showSelectedOptions = computed(() => {
      if (props.multiple === false && props.filterable === true) {
        return false;
      } else {
        return true;
      }
    });

    const showClearSelectedOptions = computed(() => {
      if (
        selectedOptions.value.length > 0 ||
        inputValue.value !== "" ||
        inputValue.value !== null
      ) {
        return true;
      }
      return false;
    });

    const changeTextareaRows = () => {
      if (inputValue.value === "" || inputValue.value === null) {
        showPlaceholder.value = true;
        clearTextarea();
        nextTick(() => {
          textarea.value.focus();
        });
      } else {
        showPlaceholder.value = false;
      }

      if (props.filterable === true) {
        if (inputValue.value === "") {
          textarea.value.style.height = "auto";
        } else {
          textarea.value.style.height = "auto";
          textarea.value.style.height = textarea.value.scrollHeight + "px";
        }
      }

      context.emit("search", inputValue.value);
    };

    const clearTextarea = () => {
      if (props.filterable === true) {
        textarea.value.style.height = "auto";
        keyTextarea.value = Math.random();
      }
    };

    watch(
      () => props.options,
      (currentValue: any, oldValue: any) => {
        console.log("watch props", props.openOnOptionsUpdate);
        if (inputValue.value != "" && currentValue.length > 0 && props.openOnOptionsUpdate) {
          dropdownOpen.value = true;
        }
      },
    );

    watch(
      () => props.value,
      () => {
        // console.log(props.value);
        inputValue.value = props.value;
        showPlaceholder.value = false;
      },
      { immediate: true },
    );

    watch(
      () => resultValue.value,
      () => {
        emitResult(resultValue.value);
      },
    );

    const emitResult = (value: any) => {
      if (
        resultValue.value === null ||
        resultValue.value === "" ||
        resultValue.value.length === 0
      ) {
        inputValue.value = "";
        showPlaceholder.value = true;
        context.emit("update:value", null);
      } else if (!props.multiple && resultValue.value.length === 1) {
        showPlaceholder.value = false;
        context.emit("update:value", resultValue.value[0]);
      } else {
        showPlaceholder.value = false;
        context.emit("update:value", value);
      }
    };

    return {
      dropdownOpen,
      toggleDropdownOpen,
      trigger,
      dropdown,
      selectedOptions,
      clickOnOption,
      closeTagOption,
      clearSelectedOptions,
      inputValue,
      showPlaceholder,
      showSelectedOptions,
      showClearSelectedOptions,
      textarea,
      keyTextarea,
      changeTextareaRows,
    };
  },
});
</script>

<style lang="scss" scoped>
.btn-select:hover .chevron-down {
  display: none;
}

.btn-select:hover .close-circle {
  display: flex;
}

.placeholder {
  color: #c2c2c2;
  display: flex;
  align-items: center;
  white-space: nowrap;
  pointer-events: none;
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 0 0 0 12px;
  height: 28px;

  .select-placeholder__inner {
    max-width: 100%;
    overflow: hidden;
  }
}

.custom-input {
  display: inline-block;
  position: relative;
  vertical-align: middle;
  border: none;
  color: #515a6e;
  background-color: #fff;
  background-image: none;
  cursor: text;
  transition: border 0.2s ease-in-out, background 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.selection-input {
  outline: none;
  position: relative;
  vertical-align: bottom;
  padding-left: 10px;
  float: left;
  width: 100%;

  .selection-input__input {
    font-size: inherit;
    font-family: inherit;
    min-width: 1px;
    padding: 0;
    background-color: #0000;
    outline: none;
    border: none;
    line-height: inherit;
    // cursor: pointer;
    width: 100%;
    resize: none;
    overflow: hidden;
    max-height: 100px;
  }
}

.wrap-loader {
  position: absolute;
  top: 1px;
  right: 8px;
  bottom: 1px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 20;
  background-color: #fff;

  .loader {
    width: 14px;
    height: 14px;
    border: 2px solid #818cf8;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
  }
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
