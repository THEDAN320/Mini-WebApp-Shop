class StorageLogger {
  static getItem(key: string): string | null {
    const value = localStorage.getItem(key);
    //console.log(`Get item: ${key} => ${value}`);
    return value;
  }

  static setItem(key: string, value: string): void {
    localStorage.setItem(key, value);
    //console.log(`Set item: ${key} => ${value}`);
  }

  static removeItem(key: string): void {
    localStorage.removeItem(key);
    //console.log(`Remove item: ${key}`);
  }

  static clear(): void {
    localStorage.clear();
    //console.log(`Clear all items`);
  }
}

export default StorageLogger;
