import moment from "moment";
import momentTz from "moment-timezone";

function formateLocalDataTime(date: any | null) {
  if (date === null || date === undefined) return null;
  return moment.utc(date).local().format("DD.MM.YYYY HH:mm:ss");
}

function formateLocalData(date: any | null) {
  if (date === null || date === undefined) return null;
  return moment.utc(date).local().format("DD.MM.YYYY");
}

function formateDataToUnixTimestamp(date: any | null) {
  if (date === null || date === undefined) return 0;
  return moment(date).unix();
}

// New Functions For Refactoring

function getTimestampNow() {
  return moment().valueOf();
}

function getTimestampForToday() {
  return moment().startOf("day").valueOf();
}

function getTimeDifferenceInHoursAndMinutes(startDate: string, endDate: string): string | null {
  const start = moment(startDate);
  const end = moment(endDate);

  if (end.isBefore(start)) {
    console.error("End time cannot be earlier than start time!");
    return null;
  }

  const duration = moment.duration(end.diff(start));
  const hours = Math.floor(duration.asHours());
  const minutes = duration.minutes();

  if (hours === 0) {
    return `${minutes}м`;
  }

  return `${hours}ч ${minutes}м`;
}

function utcDatatimeToLocalDatetime(utcDateTime: string, format = "DD.MM.YYYY HH:mm:ss") {
  const date = moment.utc(utcDateTime);
  const isValid = date.isValid();
  if (isValid) {
    return date.local().format(format);
  } else {
    throw new Error("Parameter utcDateTime is not valid datetime!");
  }
}

function localDatetimeToUtcDatatime(localDatetime: string) {
  const date = moment.utc(localDatetime);
  console.log("date =>", date);
  const isValid = date.isValid();
  if (isValid) {
    return date.toISOString();
  } else {
    throw new Error("Parameter localDatetime is not valid datetime!");
  }
}

function utcDatatimeToTimestamp(utcDateTime: string) {
  const date = moment.utc(utcDateTime);
  const isValid = date.isValid();
  if (isValid) {
    return date.valueOf();
  } else {
    throw new Error("Parameter utcDateTime is not valid datetime!");
  }
}

function timestampToUtcDatatime(timestamp: number) {
  const timestampMoment = moment.unix(timestamp / 1000);
  const isValid = timestampMoment.isValid();
  if (isValid) {
    return timestampMoment.toISOString();
  } else {
    throw new Error("Parameter timestamp is not valid datetime!");
  }
}

function timestampToLocalDatatime(timestamp: number, format = "DD.MM.YYYY HH:mm:ss") {
  const timestampMoment = moment.unix(timestamp / 1000);
  const isValid = timestampMoment.isValid();
  if (isValid) {
    return timestampMoment.local().format(format);
  } else {
    throw new Error("Parameter timestamp is not valid datetime!");
  }
}

//

const getDatetimeNow = (format = "DD.MM.YYYY HH:mm:ss") => {
  return moment().local().format(format);
};

const getCurrentYearNumber = () => {
  return moment().year();
};

const getCurrentWeekNumber = () => {
  return moment().week();
};

const getStartOfCurrentWeek = (format = "DD.MM.YYYY HH:mm:ss") => {
  return moment().startOf("isoWeek").local().format(format);
};

const getEndOfCurrentWeek = (format = "DD.MM.YYYY HH:mm:ss") => {
  return moment().endOf("isoWeek").local().format(format);
};

const getStartOfLastYearWeek = (
  year: number,
  weekNumber: number,
  format = "DD.MM.YYYY HH:mm:ss",
) => {
  return moment().isoWeekYear(year).isoWeek(weekNumber).startOf("isoWeek").local().format(format);
};

const getEndOfLastYearWeek = (year: number, weekNumber: number, format = "DD.MM.YYYY HH:mm:ss") => {
  return moment().isoWeekYear(year).isoWeek(weekNumber).endOf("isoWeek").local().format(format);
};

const getCurrentTimezoneOffset = () => {
  return Math.ceil(moment().utcOffset() / 60);
};

const getIANATimezoneName = () => {
  return Intl.DateTimeFormat().resolvedOptions().timeZone; // Ex.: Asia/Novosibirsk
};

const getDatetimeWithTimezone = (
  timestamp: number,
  timezone: string,
  format = "YYYY-MM-DD HH:mm ZZ",
) => {
  return momentTz.tz(timestamp, timezone).format(format);
};

const getDiffTimezoneByHours = (firstTimezone: string, secondTimeZone: string) => {
  const endDSTDate = momentTz.tz(getDatetimeNow("YYYY-MM-DDTHH:mm:ss"), firstTimezone);
  const startDSTDate = momentTz.tz(getDatetimeNow("YYYY-MM-DDTHH:mm:ss"), secondTimeZone);
  const diffDSTHours = endDSTDate.diff(startDSTDate, "hours");
  return diffDSTHours;
};

//

function getStartOfCurrentWeekForTimestamp(timestamp: number) {
  const timestampMoment = moment.unix(timestamp / 1000);
  const isValid = timestampMoment.isValid();
  if (isValid) {
    return timestampMoment.startOf("isoWeek").valueOf();
  } else {
    throw new Error("Parameter timestamp is not valid datetime!");
  }
}

function getEndOfCurrentWeekForTimestamp(timestamp: number) {
  const timestampMoment = moment.unix(timestamp / 1000);
  const isValid = timestampMoment.isValid();
  if (isValid) {
    return timestampMoment.endOf("isoWeek").valueOf();
  } else {
    throw new Error("Parameter timestamp is not valid datetime!");
  }
}

function isoStringToLocalDatetime(isoString: string, format = "DD.MM.YYYY") {
  const timestampMoment = moment(isoString);
  const isValid = timestampMoment.isValid();
  if (isValid) {
    return timestampMoment.local().format(format);
  } else {
    throw new Error("Parameter isoString is not a valid datetime!");
  }
}

function formatDuration(seconds: number): string {
  if (seconds < 0) {
    throw new Error("Duration cannot be negative!");
  }

  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  const parts: string[] = [];
  if (hours > 0) parts.push(`${hours}ч`);
  if (minutes > 0) parts.push(`${minutes}м`);
  if (secs > 0 || parts.length === 0) parts.push(`${secs}с`);

  return parts.join(" ");
}

function addSecondsToNow(seconds: number, format = "HH:mm:ss"): string {
  const now = moment();
  return now.add(seconds, "seconds").format(format);
}

export {
  formateLocalDataTime,
  formateLocalData,
  formateDataToUnixTimestamp,
  //
  getTimestampNow,
  getTimeDifferenceInHoursAndMinutes,
  utcDatatimeToLocalDatetime,
  localDatetimeToUtcDatatime,
  utcDatatimeToTimestamp,
  timestampToUtcDatatime,
  timestampToLocalDatatime,
  //
  getDatetimeNow,
  getCurrentYearNumber,
  getCurrentWeekNumber,
  getStartOfCurrentWeek,
  getEndOfCurrentWeek,
  getStartOfLastYearWeek,
  getEndOfLastYearWeek,
  getCurrentTimezoneOffset,
  getIANATimezoneName,
  getDatetimeWithTimezone,
  getDiffTimezoneByHours,
  getTimestampForToday,
  //
  getStartOfCurrentWeekForTimestamp,
  getEndOfCurrentWeekForTimestamp,
  //
  isoStringToLocalDatetime,
  //
  formatDuration,
  addSecondsToNow,
};
