import { Router } from '@angular/router';
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { Organization } from '../../organization/organization.model';
import { OrganizationService } from '../../organization/organization.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './org-register.component.html'
})
export class OrgRegisterComponent {
  registerForm: FormGroup;
  errorMessage: string = '';
  isLoading: boolean = false;

  constructor(
    private fb: FormBuilder,
    private organizationService: OrganizationService,
    private router: Router
  ) {
    this.registerForm = this.fb.nonNullable.group({
      name: ['', [Validators.required, Validators.minLength(4)]],
      email: ['', [Validators.required, Validators.email]],
      description: ['', [Validators.required]],
    });
  }

  navigateToOrgSelection(): void {
    this.router.navigate(['/organization/selection']);
  }


  onSubmit(): void {
    if (!this.registerForm.valid) return;

    this.isLoading = true;
    this.errorMessage = '';

    const organization: Organization = {
      name: this.name?.value,
      email: this.email?.value,
      description: this.description?.value,
    }

    this.organizationService.createOrganization(organization).subscribe({
      next: () => {
        this.router.navigate(['/organization/selection']);
      },
      error: (error) => {
        this.errorMessage = error.error?.message || 'Registro da organização falhou. Por favor, tente novamente.';
        this.isLoading = false;
      }
    });
  }


  get name() { return this.registerForm.get('name'); }
  get email() { return this.registerForm.get('email'); }
  get description() { return this.registerForm.get('description'); }

} 