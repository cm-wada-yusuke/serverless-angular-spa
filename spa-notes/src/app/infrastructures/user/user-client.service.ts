import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {environment} from '../../../environments/environment';
import {NoteUser, NoteUsers} from '../../domains/user/note-users';
import { DateUtilsService } from '../../modules/utils/date-utils.service';

@Injectable({
  providedIn: 'root'
})
export class UserClientService {

  private resourcePath =
    environment.noteApi.baseUrl + '/users';

  constructor(
    private http: HttpClient,
    private dateUtils: DateUtilsService
  ) {
  }

  getUserByOrganizationId(
    organizationId: string,
    lastEvaluatedKey: string
  ): Promise<NoteUsers> {
    const httpParams = new HttpParams()
      .set('organization_id', organizationId)
      .set('last_evaluated_key', lastEvaluatedKey);

    return this.http
      .get(this.resourcePath, {
        params: httpParams
      })
      .toPromise()
      .then(res => this.searchResponseToNoteUsers(res));
  }

  searchResponseToNoteUsers(response): NoteUsers {
    console.log(response);
    const lastEvaluatedKeyJson = response['LastEvaluatedKey'];
    const lastEvaluatedKey = lastEvaluatedKeyJson
      ? JSON.stringify(lastEvaluatedKeyJson)
      : null;
    const itemArray: Array<any> = response['Items'];
    const usersArray: Array<NoteUser> = itemArray.map(userJson => {
      const result = new NoteUser();
      result.userUuid = userJson['user_uuid'];
      result.organizationId = userJson['organization_id'];
      result.email = userJson['email'];
      result.company = userJson['company'];
      result.displayUserName = userJson['display_user_name'];
      result.createdAt = this.dateUtils.fromUnixTimeSec(userJson['created_at']);
      result.updatedAt = this.dateUtils.fromUnixTimeSec(userJson['updated_at']);
      return result;
    });
    return new NoteUsers(lastEvaluatedKey, usersArray);
  }

}
