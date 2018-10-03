import { Injectable } from '@angular/core';
import * as moment from 'moment';
import { Moment } from 'moment';

@Injectable({
  providedIn: 'root'
})
export class DateUtilsService {

  constructor() {
  }

  fromString(dateTimeString: string): Moment {
    if (!dateTimeString) {
      return null;
    } else {
      return moment(dateTimeString);
    }
  }

  fromUnixTimeSec(unixtimeSec: number): Moment {
    return moment(unixtimeSec, 'X');
  }

  formatJstDateTime(target: Moment): string {
    return target.locale('ja').format('YYYY/MM/DD HH:mm:ss');
  }

}
