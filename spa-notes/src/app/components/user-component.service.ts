import { Injectable } from '@angular/core';
import { NoteUsers } from '../domains/user/note-users';
import { UserClientService } from '../infrastructures/user/user-client.service';

@Injectable({
  providedIn: 'root'
})
export class UserComponentService {

  constructor(
    private userClient: UserClientService
  ) {
  }

  getOrganizationUsers(organizationId: string, lastEvaluatedKey: string): Promise<NoteUsers> {
    return this.userClient.getUserByOrganizationId(organizationId, lastEvaluatedKey);
  }
}
