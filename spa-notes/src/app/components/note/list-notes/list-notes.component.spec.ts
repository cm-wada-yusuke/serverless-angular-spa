
import { fakeAsync, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatSidenavModule } from '@angular/material/sidenav';
import { ListNotesComponent } from './list-notes.component';

describe('ListNotesComponent', () => {
  let component: ListNotesComponent;
  let fixture: ComponentFixture<ListNotesComponent>;

  beforeEach(fakeAsync(() => {
    TestBed.configureTestingModule({
      imports: [MatSidenavModule],
      declarations: [ListNotesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListNotesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should compile', () => {
    expect(component).toBeTruthy();
  });
});
