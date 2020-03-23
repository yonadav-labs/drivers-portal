import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { QuoteStatus } from '@/@types/quote';
import { User } from '@/@types/users';

import { APIProperty, APIState, setAuthToken, clearAuthToken } from '@/store/api'
import { getCurrentUser, getMagicLink, updateUserPassword, updateUserEmail, login, forgotPassword, getResetPasswordLink, resetPassword } from '@/store/users/api'

@Module({ namespaced: true })
export default class UsersVuexModule extends VuexModule {
  apiUser: APIProperty<User> = APIState.state<User>();
  passwordErrors?: Error;
  emailExists = false;

  get user(): User | undefined {
    return this.apiUser.data
  }

  get isAuthenticated(): boolean {
    return !!this.apiUser.data
  }

  get isUserRetrieved(): boolean {
    return this.apiUser.status !== 'initial'
  }

  get userQuoteStatus(): QuoteStatus | undefined {
    return !!this.user ? this.user.quote_status:undefined
  }

  get emailAlreadyExists(): boolean {
    return this.emailExists
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

  @Mutation
  setEmailExists(error: Error | undefined): void {
    if (error === undefined) {
      this.emailExists = false
    } else {
      this.emailExists = true
    }
  }

  @Action
  async logout(): Promise<void> {
    clearAuthToken();
    this.context.dispatch('resetStore')
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

  @Action
  async updateUserEmail(email: string): Promise<void> {
    this.context.commit('setEmailExists', undefined);
    try {
      const user = await updateUserEmail(email)
      this.context.commit('setUserPartial', user)
    } catch (e) {
      this.context.commit('setEmailExists', e);
    }
  }

  @Action
  async login(payload: { user: string, password: string }): Promise<void> {
    this.context.commit('setUserBlank')

    const { user, password } = payload

    try {
      const { token } = await login(user, password)
      setAuthToken(token);
      await this.context.dispatch('retrieveUser')
    } catch (e) {
      // pass
    }
  }

  @Action
  async forgotPassword(email: string): Promise<void> {
    try {
      await forgotPassword(email)
    } catch (e) {
      // pass
    }
  }

  @Action
  async resetPasswordLinkExists(id: string): Promise<boolean> {
    try {
      const data = await getResetPasswordLink(id)
      return !!data
    } catch (e) {
      return false
    }
  }

  @Action
  async resetPassword(payload: {id: string, password: string }): Promise<void> {
    const { id, password} = payload
    try {
      await resetPassword(id, password)
    } catch (e) {
      // pass
    }
  }
}
