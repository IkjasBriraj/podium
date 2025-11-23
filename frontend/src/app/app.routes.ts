import { Routes } from '@angular/router';
import { LandingComponent } from './pages/landing/landing';
import { AuthComponent } from './pages/auth/auth';
import { AppShellComponent } from './components/app-shell/app-shell';
import { FeedComponent } from './pages/feed/feed';
import { ProfileComponent } from './pages/profile/profile';
import { JobsComponent } from './pages/jobs/jobs';
import { NetworkComponent } from './pages/network/network';

export const routes: Routes = [
    { path: '', component: LandingComponent },
    { path: 'auth', component: AuthComponent },
    {
        path: 'app',
        component: AppShellComponent,
        children: [
            { path: '', redirectTo: 'feed', pathMatch: 'full' },
            { path: 'feed', component: FeedComponent },
            { path: 'network', component: NetworkComponent },
            { path: 'profile', component: ProfileComponent },
            { path: 'jobs', component: JobsComponent },
        ]
    }
];

