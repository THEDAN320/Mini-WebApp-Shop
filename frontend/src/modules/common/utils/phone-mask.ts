const getOnlyNumbers = (input: string) => {
  // Return stripped input value — just numbers
  return input.replace(/\D/g, "");
};

const onPhoneInput = (input: string) => {
  // eslint-disable-next-line prefer-const
  let inputNumbersValue = getOnlyNumbers(input);
  let formattedInputValue = "";

  if (!inputNumbersValue) {
    return (input = "");
  }

  if (["7"].includes(inputNumbersValue[0])) {
    const firstSymbols = "+7";
    formattedInputValue = input = firstSymbols + " ";
    if (inputNumbersValue.length > 1) {
      formattedInputValue += "(" + inputNumbersValue.substring(1, 4);
    }
    if (inputNumbersValue.length >= 5) {
      formattedInputValue += ") " + inputNumbersValue.substring(4, 7);
    }
    if (inputNumbersValue.length >= 8) {
      formattedInputValue += "-" + inputNumbersValue.substring(7, 9);
    }
    if (inputNumbersValue.length >= 10) {
      formattedInputValue += "-" + inputNumbersValue.substring(9, 11);
    }
  } else {
    formattedInputValue = "+" + inputNumbersValue.substring(0, 16);
  }
  return formattedInputValue;
};

const onPhoneInputKeyDown = (e: any) => {
  // Clear input after remove last symbol
  const inputValue = e.target.value.replace(/\D/g, "");
  if (e.keyCode === 8 && inputValue.length === 1) {
    return "";
  }
  return e.target.value;
};

export { onPhoneInput, onPhoneInputKeyDown };
