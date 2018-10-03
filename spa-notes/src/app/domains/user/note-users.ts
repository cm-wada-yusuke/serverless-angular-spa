import {Moment} from 'moment';

export class NoteUsers {
  lastEvaluatedKey: any;
  noteUsers: Array<NoteUser>;

  constructor(lastEvaluatedKey: any, noteUsers: Array<NoteUser>) {
    this.lastEvaluatedKey = lastEvaluatedKey;
    this.noteUsers = noteUsers;
  }
}

export class NoteUser {
  userUuid: string;
  organizationId: string;
  email: string;
  company: string;
  displayUserName: string;
  createdAt: Moment;
  updatedAt: Moment;
}
