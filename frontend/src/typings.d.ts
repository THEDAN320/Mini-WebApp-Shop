import "vue-router";

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
  }
}

declare module "vue-router" {
  interface RouteMeta {
    // // must be declared by every route
    // navbarName: string;
    // // is optional - does not have to be on every route
    // getter?: string;

    layout: string;
  }
}
