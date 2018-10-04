import { Component } from '@angular/core';
import { BreakpointObserver } from '@angular/cdk/layout';
import { NoteUser } from '../../../domains/user/note-users';
import { UserComponentService } from '../../user-component.service';
import { DateUtilsService } from '../../../modules/utils/date-utils.service';
import { Moment } from 'moment';

@Component({
  selector: 'app-list-notes',
  templateUrl: './list-notes.component.html',
  styleUrls: ['./list-notes.component.css']
})
export class ListNotesComponent {

  displayUsers: NoteUser[];
  lastEvaluatedKey: string;

  // Obtain from login user information, for example.
  organizationId = '1ea61e76-c2aa-433d-ad00-297ccdd32149';

  displayedColumns: string[] = [
    'displayUserName',
    'company',
    'createdAt',
    'updatedAt'
  ];
  loading = false;

  constructor(
    private breakpointObserver: BreakpointObserver,
    private service: UserComponentService,
    private dateUtil: DateUtilsService) {
  }

  refresh() {
    this.lastEvaluatedKey = null;
    this.displayUsers = [];
  }

  init() {
    this.refresh();
    this.getUsers(null);
  }

  getUsers(lastEvaluatedKey: string) {
    this.loading = true;
    this.service.getOrganizationUsers(this.organizationId, lastEvaluatedKey)
      .then(users => {
        this.displayUsers = this.displayUsers.concat(users.noteUsers);
        this.lastEvaluatedKey = users.lastEvaluatedKey;
        this.loading = false;
      });
  }

  toJst(moment: Moment): string {
    return this.dateUtil.formatJstDateTime(moment);
  }
}
