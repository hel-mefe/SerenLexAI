/**
 * Shared generic DTO helpers for API modules.
 *
 * These types intentionally mirror the raw JSON contract returned by the
 * backend and are composed in a generic way so modules don't have to repeat
 * common response shapes.
 */

/**
 * Generic paginated API response shape with a list of items.
 *
 * @template TItem Type of the items in the collection.
 */
export interface ApiPaginatedResponse<TItem> {
  /** Items on the current page. */
  items: TItem[]
  /** Total number of items across all pages. */
  total: number
  /** One-based index of the current page. */
  page: number
  /** Page size used by the backend. */
  page_size: number
}

/**
 * Generic non-paginated collection response with items and total count.
 *
 * @template TItem Type of the items in the collection.
 */
export interface ApiCollectionResponse<TItem> {
  /** Items in the collection. */
  items: TItem[]
  /** Total number of items in the collection. */
  total: number
}

/**
 * Generic DTO-to-domain mapper.
 *
 * @template TDto Raw DTO type as returned by the backend.
 * @template TDomain Domain type used inside the UI layer.
 * @param dto Raw DTO value to map.
 * @returns Mapped domain representation of the DTO.
 */
export type DtoMapper<TDto, TDomain> = (dto: TDto) => TDomain

