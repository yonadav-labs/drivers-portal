import { VuexModule, Module, Mutation, Action } from 'vuex-module-decorators';
import { QuoteProcessDocuments, QuoteProcessDocumentsAccidentReport } from '@/@types/quote';

import { APIProperty, APIState } from '@/store/api'
import { 
  retrieveQuoteProcessDocuments, updateQuoteProcessDocumentsFile, updateQuoteProcessDocuments,
  createQuoteProcessDocumentsAccidentReport, updateQuoteProcessDocumentsAccidentReport, 
  deleteQuoteProcessDocumentsAccidentReport
} from '@/store/quote/api'

@Module({ namespaced: true })
export default class QuoteDocumentsVuexModule extends VuexModule {
  apiQuoteProcessDocuments: APIProperty<QuoteProcessDocuments> = APIState.state<QuoteProcessDocuments>();

  get quoteProcessDocuments(): QuoteProcessDocuments | undefined {
    return this.apiQuoteProcessDocuments.data
  }

  @Mutation
  setQuoteProcessDocumentsBlank(): void {
    this.apiQuoteProcessDocuments = APIState.state<QuoteProcessDocuments>();
  }

  @Mutation
  setQuoteProcessDocumentsLoading(): void {
    this.apiQuoteProcessDocuments = APIState.setPending(this.apiQuoteProcessDocuments)
  }

  @Mutation
  setQuoteProcessDocuments(payload: QuoteProcessDocuments | Error): void {
    this.apiQuoteProcessDocuments = APIState.update(this.apiQuoteProcessDocuments, payload)
  }

  @Mutation
  setQuoteProcessDocumentsPartial(payload: QuoteProcessDocuments | Error): void {
    this.apiQuoteProcessDocuments = APIState.patch(this.apiQuoteProcessDocuments, payload)
  }

  @Action
  async retrieveQuoteProcessDocuments(): Promise<void> {
    this.context.commit('setQuoteProcessDocumentsLoading')

    try {
      const documents = await retrieveQuoteProcessDocuments();
      this.context.commit('setQuoteProcessDocuments', documents)
    } catch (e) {
      this.context.commit('setQuoteProcessDocuments', e);
    }
  }

  @Action
  async updateQuoteProcessDocumentsFile(payload: { field: string, file: File | '' }): Promise<void> {
    this.context.commit('setQuoteProcessDocumentsLoading')

    try {
      const documents = await updateQuoteProcessDocumentsFile(payload.field, payload.file);
      this.context.commit('setQuoteProcessDocumentsPartial', documents)
    } catch (e) {
      this.context.commit('setQuoteProcessDocumentsPartial', e);
    }
  }

  @Action
  async updateQuoteProcessDocuments(payload: { is_broker_of_record_signed?: boolean, is_submitted_for_review?: boolean, phone?: string }): Promise<void> {
    this.context.commit('setQuoteProcessDocumentsLoading')

    try {
      const submitted = await updateQuoteProcessDocuments(payload);
      this.context.commit('setQuoteProcessDocumentsPartial', submitted)
    } catch (e) {
      this.context.commit('setQuoteProcessDocumentsPartial', e);
    }
  }

  @Action
  async createQuoteProcessDocumentsAccidentReport(file: File): Promise<void> {
    this.context.commit('setQuoteProcessDocumentsLoading')

    try {
      const documents = await createQuoteProcessDocumentsAccidentReport(file);
      this.context.commit('setQuoteProcessDocumentsPartial', {
        ...this.quoteProcessDocuments,
        accident_reports: [
          ...this.quoteProcessDocuments!.accident_reports,
          documents
        ]
      })
    } catch (e) {
      this.context.commit('setQuoteProcessDocumentsPartial', e);
    }
  }

  @Action
  async updateQuoteProcessDocumentsAccidentReport(payload: {id: string, file: File}): Promise<void> {
    this.context.commit('setQuoteProcessDocumentsLoading')

    try {
      const document = await updateQuoteProcessDocumentsAccidentReport(payload.id, payload.file);
      const reports = this.quoteProcessDocuments!.accident_reports.filter(
        (report: QuoteProcessDocumentsAccidentReport) => report.id !== document.id
      )
      this.context.commit('setQuoteProcessDocumentsPartial', {
        ...this.quoteProcessDocuments,
        accident_reports: [
          ...reports,
          document
        ]
      })
    } catch (e) {
      this.context.commit('setQuoteProcessDocumentsPartial', e);
    }
  }

  @Action
  async deleteQuoteProcessDocumentsAccidentReport(id: string): Promise<void> {
    this.context.commit('setQuoteProcessDocumentsLoading')

    try {
      await deleteQuoteProcessDocumentsAccidentReport(id);
      const reports = this.quoteProcessDocuments!.accident_reports.filter(
        (report: QuoteProcessDocumentsAccidentReport) => report.id !== id
      )

      this.context.commit('setQuoteProcessDocuments', {
        ...this.quoteProcessDocuments,
        accident_reports: reports
      })
    } catch (e) {
      this.context.commit('setQuoteProcessDocuments', e);
    }
  }
}
