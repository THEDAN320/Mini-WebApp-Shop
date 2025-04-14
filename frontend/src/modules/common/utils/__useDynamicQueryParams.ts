import { ref, watch, computed, UnwrapNestedRefs } from "vue";
import { useRoute, useRouter, LocationQueryValue, LocationQuery } from "vue-router";

export enum QueryParamEnum {
  String = "string",
  Number = "number",
  Boolean = "boolean",
  StringArray = "stringArray",
  NumberArray = "numberArray",
}

type QueryParamConfigType = {
  [key: string]: {
    default: any;
    type: QueryParamEnum;
  };
};

export type newQueryParamsDataType = Record<string, string | number | string[] | number[] | null>;

export function getURIQueryParams<T extends Record<string, any>>(
  routeQuery: LocationQuery,
  queryParamsConfig: QueryParamConfigType,
) {
  const state = <Record<string, string | number | string[] | number[] | null>>{};

  Object.entries(queryParamsConfig).forEach(([key, { default: defaultValue, type }]) => {
    const value = routeQuery[key];
    if (value === undefined || value === null) {
      state[key] = null;
    } else {
      switch (type) {
        case QueryParamEnum.NumberArray:
          if (typeof value === "string") {
            state[key] = [Number(value)];
          } else {
            state[key] = value ? (value.map(Number) as number[]) : defaultValue;
          }
          break;
        case QueryParamEnum.StringArray:
          if (typeof value === "string") {
            state[key] = [value];
          } else {
            state[key] = value ? (value.map(String) as string[]) : defaultValue;
          }
          break;
        case QueryParamEnum.Number:
          state[key] = value !== undefined ? Number(value) : defaultValue;
          break;
        case QueryParamEnum.String:
          state[key] = value !== undefined ? String(value) : defaultValue;
          break;
        default:
          state[key] = defaultValue;
      }
    }
  });

  return state;
}

export function generateDataForURIQueryParams(data: Record<string, any>) {
  const result: Record<string, any> = {};

  Object.entries(data).forEach(([key, value]) => {
    if (value !== null && value !== "") {
      result[key] = value;
    }
  });
  return result;
}

export function useDynamicQueryParams<T extends Record<string, any>>(config: QueryParamConfigType) {
  const route = useRoute();
  const router = useRouter();

  const queryParams = ref<T>({} as T);

  const parseQueryParam = (
    value: LocationQueryValue | LocationQueryValue[] | null,
    type: QueryParamEnum,
  ): any => {
    if (value === null || value === undefined) return null;

    switch (type) {
      case QueryParamEnum.Number:
        return Number(value);
      case QueryParamEnum.Boolean:
        return value === "true";
      case QueryParamEnum.StringArray:
        return Array.isArray(value) ? value.map(String) : [String(value)];
      case QueryParamEnum.NumberArray:
        return Array.isArray(value) ? value.map(Number) : [Number(value)];
      default:
        return String(value);
    }
  };

  const updateQueryParams = () => {
    const newParams = { ...queryParams.value };
    Object.keys(config).forEach((key) => {
      const paramConfig = config[key];
      const routeValue = route.query[key];
      newParams[key as keyof T] =
        parseQueryParam(routeValue, paramConfig.type) ?? paramConfig.default;
    });
    queryParams.value = newParams;
  };

  watch(
    () => route.query,
    () => {
      updateQueryParams();
    },
    { immediate: true },
  );

  return {
    queryParams: computed(() => queryParams.value),
  };
}
