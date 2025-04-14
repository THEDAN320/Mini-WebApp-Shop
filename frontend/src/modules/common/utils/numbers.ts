export const formatCurrencyValue = (value: number, locale = "ru-RU") => {
  // Fallback to getCurrentLocale if locale is not provided or is null

  return Intl.NumberFormat(locale, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
};

export function formatPhoneNumber(phoneNumber: string): string {
  const cleaned = ("" + phoneNumber).replace(/\D/g, ""); // Remove any non-numeric characters
  const match = cleaned.match(/^(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})$/);

  if (match) {
    return `+${match[1]} ${match[2]} ${match[3]}-${match[4]}-${match[5]}`;
  }
  return phoneNumber; // Return the original if it doesn't match the format
}
