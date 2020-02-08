import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { User } from '@/@types/users';

import { APIProperty, APIState } from '@/store/api'
import { getCurrentUser } from '@/store/users/api'

@Module({ namespaced: true })
export default class UsersVuexModule extends VuexModule {
  apiUser: APIProperty<User> = APIState.state<User>();
  passwordErrors?: Error;

  get user(): User | undefined {
    return this.apiUser.data
  }

  get isAuthenticated(): boolean {
    return !!this.apiUser.data
  }

  get isUserRetrieved(): boolean {
    return this.apiUser.status !== 'initial'
  }

  @Mutation
  setPasswordErrors(error: Error | undefined): void {
    this.passwordErrors = error;
  }

  @Mutation
  setUserBlank(): void {
    this.apiUser = APIState.state<User>();
  }

  @Mutation
  setUserLoading(): void {
    this.apiUser = APIState.setPending(this.apiUser)
  }

  @Mutation
  setUser(payload: User | Error): void {
    this.apiUser = APIState.update(this.apiUser, payload)
  }

  @Action
  async retrieveUser(): Promise<void> {
    this.context.commit('setUserLoading')

    try {
      const user = await getCurrentUser();
      this.context.commit('setUser', user)
    } catch (e) {
      this.context.commit('setUser', e);
    }
  }

  @Action
  async updateUserPassword(password: string): Promise<void> {
    try {
      const user = await this.updateUserPassword(password)
      this.context.commit('setUser', user)
    } catch (e) {
      this.context.commit('setPasswordErrors', e);
    }
  }
}
