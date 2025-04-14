import { reactive, toRefs, toRaw, UnwrapNestedRefs, watch, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";

export enum QueryParamType {
  Number = "number",
  String = "string",
  StringArray = "stringArray",
  NumberArray = "numberArray",
}

type QueryParamConfig = {
  [key: string]: {
    default: any;
    type: QueryParamType;
  };
};

function isEqual(a: any, b: any) {
  if (a === b) return true;

  if (typeof a !== "object" || typeof b !== "object" || a == null || b == null) return false;

  const keysA = Object.keys(a);
  const keysB = Object.keys(b);

  if (keysA.length !== keysB.length) return false;

  for (const key of keysA) {
    if (!keysB.includes(key)) return false;

    if (typeof a[key] === "function" || typeof b[key] === "function") {
      throw new Error("Function comparison is not supported by this isEqual function.");
    }

    if (!isEqual(a[key], b[key])) return false;
  }

  return true;
}

export function useDynamicQueryParams<T extends Record<string, any>>(
  paramsConfig: QueryParamConfig,
) {
  const route = useRoute();
  const router = useRouter();

  const state = reactive<Record<string, any>>({});

  Object.entries(paramsConfig).forEach(([key, { default: defaultValue, type }]) => {
    const value = route.query[key];
    if (value === undefined) {
      state[key] = null;
    }
    switch (type) {
      case QueryParamType.NumberArray:
        if (typeof value === "string") {
          const formattedValue =
            value.startsWith("[") && value.endsWith("]") ? value.slice(1, -1) : value;
          state[key] = formattedValue
            ? (formattedValue.split(",").map(Number) as any)
            : defaultValue;
        } else {
          state[key] = defaultValue;
        }
        break;
      case QueryParamType.StringArray:
        if (typeof value === "string") {
          const formattedValue =
            value.startsWith("[") && value.endsWith("]") ? value.slice(1, -1) : value;
          state[key] = formattedValue ? (formattedValue.split(",") as any) : defaultValue;
        } else {
          state[key] = defaultValue;
        }
        break;
      case QueryParamType.Number:
        state[key] = value !== undefined ? (Number(value) as any) : defaultValue;
        break;
      case QueryParamType.String:
        state[key] = value !== undefined ? value : defaultValue;
        break;
      default:
        state[key] = defaultValue;
    }
  });

  watch(
    () => route.query,
    (query) => {
      Object.entries(paramsConfig).forEach(([key, { type, default: defaultValue }]) => {
        const value = query[key];
        switch (type) {
          case QueryParamType.Number:
            state[key] = value !== undefined ? Number(value) : defaultValue;
            break;
          case QueryParamType.String:
            state[key] = value !== undefined ? value : defaultValue;
            break;
          case QueryParamType.StringArray:
            if (typeof value === "string") {
              const formattedValue =
                value.startsWith("[") && value.endsWith("]") ? value.slice(1, -1) : value;
              state[key] = formattedValue !== undefined ? formattedValue.split(",") : defaultValue;
            } else {
              state[key] = defaultValue;
            }
            break;
          case QueryParamType.NumberArray:
            if (typeof value === "string") {
              const formattedValue =
                value.startsWith("[") && value.endsWith("]") ? value.slice(1, -1) : value;
              state[key] =
                formattedValue !== undefined ? formattedValue.split(",").map(Number) : defaultValue;
            } else {
              state[key] = defaultValue;
            }
            break;
          default:
            state[key] = defaultValue;
        }
      });
    },
  );
  watchEffect(() => {
    const currentQueryParams = { ...router.currentRoute.value.query };

    Object.entries(state).forEach(([key, value]) => {
      const defaultValue = paramsConfig[key]?.default;
      if (value !== null) {
        const rawValue = toRaw(value);
        const rawDefaultValue = toRaw(defaultValue);

        if (Array.isArray(rawValue)) {
          const isEqualToDefault = isEqual(rawValue, rawDefaultValue);
          if (!isEqualToDefault) {
            currentQueryParams[key] = "[" + rawValue.join(",") + "]";
          } else {
            delete currentQueryParams[key];
          }
        } else {
          const isEqualToDefault = isEqual(rawValue, rawDefaultValue);
          if (!isEqualToDefault) {
            currentQueryParams[key] = rawValue;
          } else {
            delete currentQueryParams[key];
          }
        }
      } else {
        delete currentQueryParams[key];
      }
    });

    router.replace({ query: currentQueryParams }).catch((err) => {
      if (err.name !== "NavigationDuplicated") throw err;
    });
  });

  return { ...toRefs(state) };
}
