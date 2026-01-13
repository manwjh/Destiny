/**
 * 版本信息 | Version Information
 * 《算一卦/Destiny》- Calculate a Fortune/Destiny
 */

export const VERSION = '0.1.0';
export const VERSION_TAG = 'v0.1.0';
export const RELEASE_DATE = '2026-01-13';

export const PROJECT_NAME = 'Destiny';
export const PROJECT_NAME_CN = '算一卦';
export const PROJECT_DESCRIPTION = 'A fun fortune-telling software - An oracle that doesn\'t comfort you, just gives results';
export const PROJECT_DESCRIPTION_CN = '一个好玩的算命软件 - 不安慰你，只给结果的算卦器';

export const API_VERSION = 'v1';

export interface VersionInfo {
  version: string;
  versionTag: string;
  releaseDate: string;
  projectName: string;
  projectNameCn: string;
  description: string;
  descriptionCn: string;
  apiVersion: string;
}

export function getVersion(): string {
  return VERSION;
}

export function getFullVersion(): VersionInfo {
  return {
    version: VERSION,
    versionTag: VERSION_TAG,
    releaseDate: RELEASE_DATE,
    projectName: PROJECT_NAME,
    projectNameCn: PROJECT_NAME_CN,
    description: PROJECT_DESCRIPTION,
    descriptionCn: PROJECT_DESCRIPTION_CN,
    apiVersion: API_VERSION,
  };
}
