import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { User } from '@/@types/users';

import { APIProperty, APIState, setAuthToken } from '@/store/api'
import { getCurrentUser, getMagicLink, updateUserPassword } from '@/store/users/api'

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

  @Mutation
  setUserPartial(payload: User | Error): void {
    this.apiUser = APIState.patch(this.apiUser, payload)
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
  async useMagickLink(id: string): Promise<void> {
    this.context.commit('setUserBlank')

    try {
      const { token } = await getMagicLink(id)
      setAuthToken(token);
      await this.context.dispatch('retrieveUser')
    } catch (e) {
      console.error(new Error('Invalid Magic Link'))
    }
  }

  @Action
  async updateUserPassword(password: string): Promise<void> {
    try {
      const user = await updateUserPassword(password)
      this.context.commit('setUserPartial', user)
    } catch (e) {
      this.context.commit('setPasswordErrors', e);
    }
  }
}
